# flake8: noqa: I001, I004
import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from core.constants import (
    CHARS_FOR_RECIPY_NAME,
    MAX_COOKING_TIME,
    MIN_COOKING_TIME
)
from recipes.models import (
    Dosage,
    Favorite,
    Ingredient,
    Recipy,
    RecipyTags,
    ShoppingCart,
    Tag
)
from users import serializers as users_serializers


class Base64ImageField(serializers.ImageField):
    """Сериализирует изображение формата base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipesShort(serializers.ModelSerializer):
    """Сериализатор для краткого отображения рецепта, в модели пользователя-автора."""
    image = Base64ImageField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipy


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
    author = users_serializers.CustomUserSerializer(read_only=True, many=False)

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


def dosagecreation(dosagelist, recipy):
    """Создает ингредиент с дозировкой в рецепте."""
    for ingredient in dosagelist:
        amount = ingredient['amount']
        id = ingredient['id']
        current_ingredient = get_object_or_404(
            Ingredient, id=id
        )
        Dosage.objects.create(
            ingredient=current_ingredient,
            amount=amount,
            recipy=recipy
        )


class RecipySerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования рецепта."""
    image = Base64ImageField(required=True, allow_null=False)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=Tag.objects.all()
    )
    ingredients = DosageCreateSerializer(
        many=True, source='recipyingredient'
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

    def validate(self, data):
        if data['cooking_time'] < MIN_COOKING_TIME:
            raise ValidationError(
                f'Время готовки должно быть не менее {MIN_COOKING_TIME}!')
        if data['cooking_time'] > MAX_COOKING_TIME:
            raise ValidationError(
                f'Время готовки более {MAX_COOKING_TIME/60} часов? Помилуйте!')
        if len(data['name']) > CHARS_FOR_RECIPY_NAME:
            raise ValidationError(
                'Слишком длинное название'
            )
        return data

    def create(self, validated_data):
        current_user = self.context['request'].user
        tags = validated_data.pop('tags')
        recipyingredients = validated_data.pop('recipyingredient')
        recipy = Recipy.objects.create(author=current_user, **validated_data)
        for tag in tags:
            RecipyTags.objects.create(tag=tag, recipy=recipy)
        dosagecreation(recipyingredients, recipy)
        return recipy

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        recipyingredients = validated_data.pop('recipyingredient')
        RecipyTags.objects.filter(recipy=instance).delete()
        Dosage.objects.filter(recipy=instance).delete()
        instance.name = validated_data.get('name', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        for tag in tags:
            RecipyTags.objects.create(tag=tag, recipy=instance)
        dosagecreation(recipyingredients, instance)
        instance.save()
        return instance
