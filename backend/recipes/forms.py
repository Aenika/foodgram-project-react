from django import forms

from .models import Recipy


class RecipyForm(forms.ModelForm):
    labels = {
        'name': 'Название рецепта',
        'text': 'Текст рецепта',
        'cooking_time': 'Время готовки'
    }
    help_texts = {
        'name': 'Введите название рецепта',
        'text': 'Введите описание процесса готовки',
        'cooking_time': 'Введите время готовки в минутах'
    }

    class Meta:
        model = Recipy
        widgets = {'text': forms.Textarea}
        fields = ('name', 'text', 'cooking_time')
