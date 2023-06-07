import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import (Dosage, Favorite, Ingredient, Recipy, RecipyTags,
                            ShoppingCart, Tag)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from users.models import Follow, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class RecipesShort(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipy


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = RecipesShort(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'

        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj
        ).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Ingredient


class DosageSerializer(serializers.ModelSerializer):
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


class DosageCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Dosage
        fields = ('id', 'amount')


class RecipyGetSerializer(serializers.ModelSerializer):
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
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipy=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipy=obj
        ).exists()


class RecipyShortSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    author = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'image',
            'name',
            'tags',
            'cooking_time',
            'author',
            'is_in_shopping_cart',
            'is_favorited'
        ]
        model = Recipy

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipy=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipy=obj
        ).exists()

    def get_author(self, obj):
        author = obj.author
        return author.get_full_name()


class RecipySerializer(serializers.ModelSerializer):
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
        if data['cooking_time'] < 1:
            raise ValidationError(
                'Время готовки должно быть больше 1 минуты!')
        if data['cooking_time'] > 720:
            raise ValidationError(
                'Время готовки более 12 часов? Помилуйте!')
        return data

    def create(self, validated_data):
        current_user = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipy = Recipy.objects.create(author=current_user, **validated_data)
        for tag in tags:
            RecipyTags.objects.create(tag=tag, recipy=recipy)
        for ingredient in ingredients:
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
        return recipy


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('user', 'author')
        model = Follow
        read_only_fields = ('user',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message='Такая подписка уже есть'
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['author']:
            raise ValidationError(
                'На себя нельзя подписываться, даже если ты очень хорош!'
            )
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = ShoppingCart
        read_only_fields = ('user',)
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipy'],
                message='Рецепт уже в списке покупок'
            )
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Favorite
        read_only_fields = ('user',)
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipy'],
                message='Рецепт уже в списке избранного'
            )
        ]
