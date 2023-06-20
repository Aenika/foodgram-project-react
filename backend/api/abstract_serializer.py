from rest_framework import serializers

from recipes.abstract_models import RecipyToUserModel
from recipes.models import Recipy


class RecipyToUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели избранного."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=Recipy.objects.all()
    )

    class Meta:
        fields = ('user', 'recipy')
        model = RecipyToUserModel
        read_only_fields = ('user',)
