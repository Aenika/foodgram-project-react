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
        help_text='Введите описание блюда и метод приготовления'
    )
    cooking_time = models.DurationField(
        verbose_name='Время приготовления рецепта',
        help_text='Введите время, которое занимает готовка по данному рецепту'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(
    # verbose_name='Картинка',
    # upload_to='recipes/',
    # blank=True,
    # help_text='Загрузите картинку'
    # )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
