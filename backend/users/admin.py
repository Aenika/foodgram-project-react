from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    """Класс для отображения пользователей в админ зоне."""
    list_display = ('email', 'username', 'role',)
    search_fields = ('email', 'username', 'role',)
    list_filter = ('email', 'username')


class FollowAdmin(admin.ModelAdmin):
    """Класс для отображения подписок в админ зоне."""
    list_display = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
