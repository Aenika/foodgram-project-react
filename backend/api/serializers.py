# flake8: noqa: I001, I004
import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import ValidationError

from core.constants import (CHARS_FOR_EMAIL, CHARS_FOR_FIRST_NAME,
                            CHARS_FOR_LAST_NAME, CHARS_FOR_PASSWORD,
                            CHARS_FOR_RECIPY_NAME, CHARS_FOR_USERNAME,
                            MAX_COOKING_TIME, MIN_COOKING_TIME)
from recipes.models import (Dosage, Favorite, Ingredient, Recipy, RecipyTags,
                            ShoppingCart, Tag)
from users.models import Follow, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Ingredient


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['email', 'username', 'first_name', 'last_name', 'password']

    def validate(self, data):
        fields = {
            'email': CHARS_FOR_EMAIL,
            'username': CHARS_FOR_USERNAME,
            'first_name': CHARS_FOR_FIRST_NAME,
            'last_name': CHARS_FOR_LAST_NAME,
            'password': CHARS_FOR_PASSWORD
        }
        for key, value in fields.items():
            if len(data[key]) > value:
                raise serializers.ValidationError(
                    f'Это поле должно быть не более {value} символов!'
                )
        return data


class RecipesShort(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipy


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj
        ).exists()


class UserRecipesSerializer(CustomUserSerializer):
    recipes = RecipesShort(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField()

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

    def get_recipes_count(self, obj):
        return obj.recipes.count()


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


class RecipyShortSerializer(RecipyGetSerializer):
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

    def get_author(self, obj):
        author = obj.author
        return author.get_full_name()


class DosageCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Dosage
        fields = ('id', 'amount')


def dosagecreation(dosagelist, recipy):
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
