from django.contrib import admin

from .models import (Dosage, Favorite, Ingredient, Recipy, RecipyTags,
                     ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class TagInline(admin.TabularInline):
    model = RecipyTags


class IngredientInline(admin.StackedInline):
    model = Dosage
    fields = ('ingredient', 'amount')


class RecipyAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'text', 'cooking_time', 'fav_count')
    list_filter = ('name', 'author__username', 'tags__name')
    inlines = [
        TagInline,
        IngredientInline
    ]

    def fav_count(self, obj):
        Favorite.objects.filter(recipy=obj).count()


class RecipyToUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipy')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipy, RecipyAdmin)
admin.site.register(ShoppingCart, RecipyToUserAdmin)
admin.site.register(Favorite, RecipyToUserAdmin)
