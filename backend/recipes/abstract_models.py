from django.db import models


class RecipyToUserModel(models.Model):
    """
    Класс для представления связи рецепт-пользователь.
    Родительский класс для классов избранного и списка покупок.
    """
    recipy = models.ForeignKey(
        "recipes.Recipy",
        verbose_name="рецепт",
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User",
        verbose_name="пользователь",
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

    def __str___(self):
        return f'{self.user} добавил {self.recipy}'
