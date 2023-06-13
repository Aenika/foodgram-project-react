# flake8: noqa: I001, I004
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.serializer_recipy import RecipesShort
from .constants import (
    CHARS_FOR_EMAIL,
    CHARS_FOR_FIRST_NAME,
    CHARS_FOR_LAST_NAME,
    CHARS_FOR_PASSWORD,
    CHARS_FOR_USERNAME
)
from .models import Follow, User


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""
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
        try:
            User.objects.get(email=data['email'])
        except User.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует!'
            )
        if data['username'].lower() == 'me':
            raise serializers.ValidationError(
                'Данное имя нельзя использовать!'
            )
        try:
            User.objects.get(username=data['username'])
        except User.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError(
                'Пользователь с таким логином уже существует!'
            )
        return data


class CustomUserSerializer(UserSerializer):
    """Сериализатор для отображения пользователя."""
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
        if request is None:
            return False
        return request.user.is_authenticated and Follow.objects.filter(
            user=request.user, author=obj
        ).exists()


class UserRecipesSerializer(CustomUserSerializer):
    """Сериализатор для отображения пользователя со списком его рецептов."""
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


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели подписок."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    author = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=User.objects.all()
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
            raise serializers.ValidationError(
                'На себя нельзя подписываться, даже если ты очень хорош!'
            )
        return data
