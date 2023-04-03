from django.contrib import admin

from .models import Recipy


class RecipyAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author')
# добавить фильтрацию по тегам
# На странице рецепта вывести общее число добавлений этого рецепта в избранное.


admin.site.register(Recipy, RecipyAdmin)
