import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from recipes.models import Favorite, Ingredient, Recipy, ShoppingCart, Tag
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


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class RecipySerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        fields = ('__all__')
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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Ingredient


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), read_only=False, slug_field='username'
    )

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
