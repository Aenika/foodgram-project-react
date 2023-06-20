import django_filters

from recipes.models import Ingredient, Recipy


class RecipyFilter(django_filters.FilterSet):
    """
    Фильтр настраивает поиск по тегу и по id автора,
    а также по параметрам is_favorited=1 и is_in_shopping_cart=1.
    """
    tags = django_filters.CharFilter(
        field_name='tags__slug', lookup_expr='contains'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_shopping_cart',
    )
    is_favorited = django_filters.NumberFilter(
        method='get_favorited',
    )

    class Meta:
        model = Recipy
        fields = ('tags', 'author')

    def get_shopping_cart(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(recipes_shoppingcarts__user=user)
        return queryset

    def get_favorited(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(recipes_favorites__user=user)
        return queryset


class IngredientFilter(django_filters.FilterSet):
    """Фильтр настраивает поиск по началу названия ингредиента."""
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
