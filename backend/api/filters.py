# flake8: noqa: I001, I004
import django_filters

from recipes.models import Recipy


class RecipyByTagSlugFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(
        field_name="tags__slug", lookup_expr='contains'
    )

    class Meta:
        model = Recipy
        fields = ('tags', 'author')
