from recipes.models import Ingredient, Recipy, Tag
from rest_framework import mixins, viewsets

from .serializers import IngredientSerializer, RecipySerializer, TagSerializer
from .viewsets import CreateDestroyListViewSet


class RecipyViewSet(viewsets.ModelViewSet):
    queryset = Recipy.objects.all()
    serializer_class = RecipySerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class SubscriptonViewSet(CreateDestroyListViewSet):
    pass


class ShoppingCartViewSet(CreateDestroyListViewSet):
    pass


class PostDeleteFav(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass
