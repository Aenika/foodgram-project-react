from djoser.serializers import UserSerializer
from recipes.models import Ingredient, Recipy, Tag
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class RecipySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Recipy


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Ingredient
