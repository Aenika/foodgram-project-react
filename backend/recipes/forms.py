from django import forms

from .models import Recipy


class RecipyForm(forms.ModelForm):
    class Meta:
        model = Recipy
        fields = ('name', 'text', 'cooking_time')
