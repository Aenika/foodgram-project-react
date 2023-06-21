from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipy, Tag


class RecipyFilter(FilterSet):
    """
    Фильтр настраивает поиск по тегу и по id автора,
    а также по параметрам is_favorited=1 и is_in_shopping_cart=1.
    """
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
        conjoined=False
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='get_shopping_cart',
    )
    is_favorited = filters.NumberFilter(
        method='get_favorited',
    )

    class Meta:
        model = Recipy
        fields = ('tags', 'author')

    def get_shopping_cart(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(recipes_shoppingcarts__user=user)
        return queryset

    def get_favorited(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(recipes_favorites__user=user)
        return queryset


class IngredientFilter(FilterSet):
    """Фильтр настраивает поиск по началу названия ингредиента."""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
