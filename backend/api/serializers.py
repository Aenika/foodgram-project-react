from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import (
    UniqueTogetherValidator,
    UniqueValidator,
    ValidationError
)

from core.constants import (
    CHARS_FOR_RECIPY_NAME,
    MIN_COOKING_TIME
)
from core.serializer_recipy import Base64ImageField
from recipes.models import (
    Dosage,
    Favorite,
    Ingredient,
    Recipy,
    RecipyTags,
    ShoppingCart,
    Tag
)
from users.serializers import CustomUserSerializer
from .abstract_serializer import RecipyToUserSerializer
from .exceptions import NameDuplicationError


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Теги"""
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиенты."""
    class Meta:
        fields = '__all__'
        model = Ingredient


class DosageSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов с дозировкой в рецепте."""
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = Dosage
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipyGetSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта."""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = DosageSerializer(
        read_only=True,
        many=True,
        source='recipyingredient'
    )
    author = CustomUserSerializer(read_only=True, many=False)

    class Meta:
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
        model = Recipy

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        return request.user.is_authenticated and Favorite.objects.filter(
            user=request.user, recipy=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        return request.user.is_authenticated and ShoppingCart.objects.filter(
            user=request.user, recipy=obj
        ).exists()


class DosageCreateSerializer(serializers.ModelSerializer):
    """Серализатор для создания ингредиента с дозировкой в рецепте."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Dosage
        fields = ('id', 'amount')

    def validate_amount(self, data):
        if int(data) < 1:
            raise ValidationError(
                'Введите количество 1 или более!'
            )
        return data


def dosagecreation(dosagelist, recipy):
    """Создает ингредиент с дозировкой в рецепте."""
    bulk_list = []
    for ingredient in dosagelist:
        dosage = Dosage(
            recipy=recipy,
            ingredient_id=ingredient['id'],
            amount=ingredient['amount']
        )
        bulk_list.append(dosage)
    Dosage.objects.bulk_create(bulk_list)


class RecipySerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования рецепта."""
    image = Base64ImageField(required=True, allow_null=False)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Tag.objects.all(),
        validators=[UniqueValidator(queryset=RecipyTags.objects.all())]
    )
    ingredients = DosageCreateSerializer(
        many=True,
        source='recipyingredient'
    )

    class Meta:
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        ]
        model = Recipy
        read_only_fields = ('author',)

    def validate_name(self, value):
        if len(value) > CHARS_FOR_RECIPY_NAME:
            raise ValidationError(
                'Слишком длинное название'
            )
        return value

    def validate_tags(self, value):
        tag_list = []
        for tag in value:
            if tag.slug in tag_list:
                raise ValidationError('Такой тег уже есть!')
            tag_list.append(tag.slug)
        if not value:
            raise ValidationError('Нужен хотя бы один тег!')
        return value

    def validate_cooking_time(self, value):
        if int(value) < int(MIN_COOKING_TIME):
            raise ValidationError(
                f'Время готовки должно быть не менее {MIN_COOKING_TIME}!')
        return value

    def validate_ingredients(self, value):
        ingredient_list = []
        for ingredient in value:
            if ingredient['id'] in ingredient_list:
                raise NameDuplicationError()
            ingredient_list.append(ingredient['id'])
        if not value:
            raise ValidationError('Нужен хотя бы один ингредиент!')
        return value

    @transaction.atomic
    def create(self, validated_data):
        current_user = self.context['request'].user
        tags = validated_data.pop('tags')
        recipyingredients = validated_data.pop('recipyingredient')
        recipy = Recipy.objects.create(author=current_user, **validated_data)
        RecipyTags.objects.bulk_create(
            [RecipyTags(tag=tag, recipy=recipy) for tag in tags]
        )
        dosagecreation(recipyingredients, recipy)
        return recipy

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        recipyingredients = validated_data.pop('recipyingredient')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        dosagecreation(recipyingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipyGetSerializer(
            instance, context=context
        ).data


class FavoriteSerializer(RecipyToUserSerializer):
    """Сериализатор для модели избранного."""

    class Meta:
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipy'],
                message='Рецепт уже в избранном!'
            )
        ]


class ShoppingCartSerializer(RecipyToUserSerializer):
    """Сериализатор для модели списка покупок."""

    class Meta:
        model = ShoppingCart
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipy'],
                message='Рецепт уже в списке покупок!'
            )
        ]
