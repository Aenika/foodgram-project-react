from django.contrib import admin

from .models import Dosage, Favorite, Ingredient, Recipy, RecipyTags, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    list_filter = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


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


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipy, RecipyAdmin)
