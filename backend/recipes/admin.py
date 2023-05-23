from django.contrib import admin

from .models import Recipy, Tag


class RecipyAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author')
# добавить фильтрацию по тегам
# На странице рецепта вывести общее число добавлений этого рецепта в избранное


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'hexcolor')
    list_filter = ('name',)


admin.site.register(Recipy, RecipyAdmin)
admin.site.register(Tag, TagAdmin)
