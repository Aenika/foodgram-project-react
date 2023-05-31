from django.db import models


class FavoriteShoppingModel(models.Model):
    recipy = models.ManyToManyField(
        "recipes.Recipy",
        verbose_name='рецепт'
    )
    user = models.ManyToManyField(
        "users.User",
        verbose_name='пользователь'
    )

    class Meta:
        abstract = True
