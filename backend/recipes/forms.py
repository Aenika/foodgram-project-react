from django import forms

from .models import Recipy, Tag


class RecipyForm(forms.ModelForm):
    labels = {
        'name': 'Название рецепта',
        'text': 'Текст рецепта',
        'tags': 'Теги',
        'cooking_time': 'Время готовки',
        'image': 'Фото готового блюда'
    }
    help_texts = {
        'name': 'Введите название рецепта',
        'text': 'Введите описание процесса готовки',
        'tags': 'Выберите все подходящие теги',
        'cooking_time': 'Введите время готовки в минутах',
        'image': 'Добавьте фотографию'
    }

    class Meta:
        tags_exist = Tag.objects.values('name')
        model = Recipy
        widgets = {
            'text': forms.Textarea,
            'tags': forms.CheckboxSelectMultiple(choices=tags_exist)
        }
        fields = ('name', 'text', 'cooking_time', 'image', 'tags')
