# flake8: noqa: I001, I004
import django_filters

from recipes.models import Recipy


class RecipyFilter(django_filters.FilterSet):
    """
    Фильтр настраивает поиск по тегу и по id автора,
    а также по параметрам is_favorited=true и is_in_shopping_cart=true.
    """
    tags = django_filters.CharFilter(
        field_name='tags__slug', lookup_expr='contains'
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_shopping_cart',
    )
    is_favorited = django_filters.BooleanFilter(
        method='get_favorited',
    )

    def get_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        user = self.request.user
        return Recipy.objects.filter(recipes_shoppingcarts__user=user)

    def get_favorited(self, queryset, name, value):
        if not value:
            return queryset
        user = self.request.user
        return Recipy.objects.filter(recipes_favorites__user=user)

    class Meta:
        model = Recipy
        fields = ('tags', 'author')
