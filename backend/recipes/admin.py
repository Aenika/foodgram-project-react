from django.contrib import admin

from .models import Ingredient, Recipy, Tag


class RecipyAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
# добавить фильтрацию по тегам
# На странице рецепта вывести общее число добавлений этого рецепта в избранное


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    list_filter = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


admin.site.register(Recipy, RecipyAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
