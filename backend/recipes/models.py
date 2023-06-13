# flake8: noqa: I001, I004

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)
from django.db import models


from core.constants import (
    CHARS_FOR_RECIPY_NAME,
    MAX_COOKING_TIME,
    MIN_COOKING_TIME
)
from users.models import User
from .abstract_models import RecipyToUserModel
from .constants import (
    CHARS_FOR_INGREDIENT_NAME,
    CHARS_FOR_MEASURE,
    CHARS_FOR_TAG_NAME,
    CHARS_FOR_TAG_SLUG
)


class Ingredient(models.Model):
    """Класс для представления ингредиентов."""
    name: str = models.CharField(
        max_length=CHARS_FOR_INGREDIENT_NAME,
        verbose_name='Название ингредиента',
        unique=False,
    )
    measurement_unit: str = models.CharField(
        max_length=CHARS_FOR_MEASURE,
        verbose_name='Единицы измерения',
        unique=False
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_Ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Класс для представления тегов."""
    name: str = models.CharField(
        max_length=CHARS_FOR_TAG_NAME,
        verbose_name='Название тега',
        unique=True
    )
    color: str = models.CharField(
        max_length=7,
        unique=True,
        default='#ffffff',
        verbose_name='Цвет тега',
        validators=[
            RegexValidator(regex=r'^\#[\w]{6}$'),
        ]
    )
    slug: str = models.SlugField(
        unique=True, verbose_name='Слаг тега', max_length=CHARS_FOR_TAG_SLUG
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color'], name='unique_Tag'
            )
        ]

    def __str__(self):
        return self.name


class Recipy(models.Model):
    """Класс для представления рецептов."""
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
        through='RecipyTags'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Dosage',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    name: str = models.CharField(
        max_length=CHARS_FOR_RECIPY_NAME,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )
    text: str = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Введите описание блюда и метод приготовления'
    )
    cooking_time: int = models.IntegerField(
        verbose_name='Время приготовления рецепта',
        help_text='Введите время приготовления в минутах',
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                f'Время готовки не может быть меньше {MIN_COOKING_TIME}!'
            ),
            MaxValueValidator(
                MAX_COOKING_TIME,
                f'Время готовки более {MAX_COOKING_TIME/60} часов? Помилуйте!'
            )
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipyTags(models.Model):
    """Класс для промежуточной связи полей многие-ко-многим рецепты-теги."""
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE, verbose_name="Рецепт")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")

    class Meta:
        verbose_name = 'тег рецепта'
        verbose_name_plural = 'теги рецепта'

    def __str__(self):
        return f'{self.tag} у рецепта {self.recipy}'


class Dosage(models.Model):
    """Класс для связи полей многие-ко-многим рецепты-ингредиенты, добавляет поле количество."""
    recipy = models.ForeignKey(
        Recipy,
        on_delete=models.CASCADE,
        related_name='recipyingredient',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount: int = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Введите необходимое количество ингредиента'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit})'
            f' — {self.amount} '
        )


class ShoppingCart(RecipyToUserModel):
    """Класс для представления рецептов в списке покупок пользователя."""

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipy"], name="unique_in_shopping_cart"
            )
        ]

    def __str___(self):
        return f'{self.user} добавил в покупки рецепт {self.recipy}'


class Favorite(RecipyToUserModel):
    """Класс для представления рецептов в списке избранного пользователя."""

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipy"], name="unique_favorite"
            )
        ]

    def __str___(self):
        return f'{self.user} добавил в избранное рецепт {self.recipy}'
