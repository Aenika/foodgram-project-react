from django.db import models


class RecipyToUserModel(models.Model):
    recipy = models.ForeignKey(
        "recipes.Recipy",
        verbose_name='рецепт',
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name='пользователь',
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipy"], name="unique_pair"
            )
        ]
