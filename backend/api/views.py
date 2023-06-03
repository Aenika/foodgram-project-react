from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipy, ShoppingCart, Tag
from rest_framework import permissions, viewsets
from users.models import Follow

from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipySerializer,
                          ShoppingCartSerializer, TagSerializer)
from .viewsets import CreateDestroyListViewSet


class RecipyViewSet(viewsets.ModelViewSet):
    queryset = Recipy.objects.all()
    serializer_class = RecipySerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SubscriptonViewSet(CreateDestroyListViewSet):
    queryset = Follow.objects.all
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.request.user.follower.all()


class ShoppingCartViewSet(CreateDestroyListViewSet):
    queryset = ShoppingCart.objects.all
    serializer_class = ShoppingCartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.recipes_shoppingcart_related.all()


class FavoriteViewSet(CreateDestroyListViewSet):
    queryset = Favorite.objects.all
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.request.user.recipes_favorite_related.all()
