from django.db import models
from users.models import User


class Recipy(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Введите описание блюда и методов приготовления'
    )
    cooking_time = models.DurationField(
        verbose_name='Время приготовления рецепта',
        help_text='Введите время приготовления в минутах'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь, кто подписывается',
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписки',
    )

    def __str__(self):
        return f'Пользователь {self.user} подписан на автора {self.author}.'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_follow"
            )
        ]
