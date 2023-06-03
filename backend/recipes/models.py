from core.models import RecipyToUserModel
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        unique=False,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
        unique=False
    )

    class Meta:
        ordering = ("name",)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"], name="unique_Ingredient"
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        unique=True
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг тега')
    color = models.CharField(
        max_length=7,
        unique=True,
        default="#ffffff",
        verbose_name='Цвет тега',
        validators=[
            RegexValidator(regex=r'^\#[\w]{6}$')
        ]
    )

    class Meta:
        ordering = ("name",)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


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
        help_text='Введите время приготовления в минутах',
        validators=[
            MinValueValidator(1, 'Время готовки не может быть меньше минуты!'),
            MaxValueValidator(720, '')
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги', related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="Dosage",
        verbose_name='Ингредиенты',
        related_name='recipes'
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Dosage(models.Model):
    recipy = models.ForeignKey(Recipy, on_delete=models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    amount: int = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Введите необходимое количество ингредиента'
    )

    def measurement_unit(self):
        return self.ingredient.measurement_unit

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'{self.ingredient} : {self.amount} {self.measurement_unit}'


class ShoppingCart(RecipyToUserModel):

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str___(self):
        return f'{self.user} добавил в покупки рецепт {self.recipy}'


class Favorite(RecipyToUserModel):

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = verbose_name

    def __str___(self):
        return f'{self.user} добавил в избранное рецепт {self.recipy}'
