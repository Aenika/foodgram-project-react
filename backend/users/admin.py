from django.contrib import admin

from recipes.models import Recipy
from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    """Класс для отображения пользователей в админ зоне."""
    list_display = (
        'email',
        'username',
        'role',
        'recipes_count',
        'followers_count',
    )
    search_fields = ('email', 'username', 'role',)
    list_filter = ('email', 'username')

    def recipes_count(self, obj):
        return Recipy.objects.filter(author=obj).count()
    recipes_count.short_description = 'Количество рецептов'

    def followers_count(self, obj):
        return Follow.objects.filter(author=obj).count()
    followers_count.short_description = 'Количество подписок'


class FollowAdmin(admin.ModelAdmin):
    """Класс для отображения подписок в админ зоне."""
    list_display = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
