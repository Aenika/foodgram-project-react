# flake8: noqa: I001, I005
from django.contrib import admin

from .models import (
    Dosage,
    Favorite,
    Ingredient,
    Recipy,
    RecipyTags,
    ShoppingCart,
    Tag
)


class TagAdmin(admin.ModelAdmin):
    """Класс для отображения тегов в админ зоне."""
    list_display = ('name', 'slug', 'color')


class IngredientAdmin(admin.ModelAdmin):
    """Класс для отображения ингредиентов в админ зоне."""
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class TagInline(admin.TabularInline):
    """Класс для отображения тегов в рецептах в админ зоне."""
    model = RecipyTags


class IngredientInline(admin.StackedInline):
    """Класс для отображения тегов в рецептах админ зоне."""
    model = Dosage
    fields = ('ingredient', 'amount')


class RecipyAdmin(admin.ModelAdmin):
    """Класс для отображения рецептов в админ зоне."""
    model = Recipy
    list_display = ('name', 'author', 'text', 'cooking_time', 'fav_count')
    list_filter = ('name', 'author__username', 'tags__name')
    inlines = [
        TagInline,
        IngredientInline
    ]

    def fav_count(self, obj):
        return Favorite.objects.filter(recipy=obj).count()
    fav_count.short_description = 'Количество добавлений в избранное'


class RecipyToUserAdmin(admin.ModelAdmin):
    """Класс для отображения списков покупок и избранного в админ зоне."""
    list_display = ('user', 'recipy')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipy, RecipyAdmin)
admin.site.register(ShoppingCart, RecipyToUserAdmin)
admin.site.register(Favorite, RecipyToUserAdmin)
