import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Recipy


class Base64ImageField(serializers.ImageField):
    """Сериализирует изображение формата base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipesShort(serializers.ModelSerializer):
    """
    Сериализатор для краткого отображения рецепта,
    в модели пользователя-автора.
    Вынесен в приложение core для избежания кругового импорта,
    который вызывает ошибки.
    """
    image = Base64ImageField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipy
