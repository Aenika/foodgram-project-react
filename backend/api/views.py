from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.pagination import CustomPagination
from core.viewsets import CreateDestroyViewSet
from recipes.models import (
    Favorite,
    Ingredient,
    Recipy,
    ShoppingCart,
    Tag
)
from .filters import IngredientFilter, RecipyFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipyGetSerializer,
    RecipySerializer,
    ShoppingCartSerializer,
    TagSerializer
)
from .service import create_content, create_downloadable_file


class RecipyViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для класса рецептов. Возможные действия:
    list: вывести список рецептов,
    retrieve: вывести один рецепт,
    update: изменить рецепт,
    create: создать рецепт,
    destroy: удалить рецепт.
    """
    queryset = Recipy.objects.select_related('author').all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipyFilter
    serializer_class = RecipyGetSerializer

    def get_serializer_class(self):
        """Выбирает необходимый сериалайзер для действия."""
        if self.action == 'list' or self.action == 'retrieve':
            return RecipyGetSerializer
        return RecipySerializer

    @action(detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        """
        Формирует скачиваемый pdf файл со списком ингредентов и дозировкой
        для выбранных в "список покупок" рецептов.
        """
        user = request.user
        content = create_content(user)
        buffer = create_downloadable_file(content)
        return FileResponse(
            buffer, as_attachment=True, filename='shopping_cart.pdf'
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения списка и единично тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения спика и единично ингредиентов."""
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientFilter
    permission_classes = (permissions.AllowAny,)


class CreateDesroyFavViewSet(CreateDestroyViewSet):
    """
    Вьюсет с двумя методами, создание и удаление.
    create: добавляет выбранный рецепт в избранное,
    destroy: удаляет выбранный рецепт из избранного.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteSerializer

    def create(self, request, id):
        user = request.user
        recipy = get_object_or_404(Recipy, id=id)
        Favorite.objects.create(user=user, recipy=recipy)
        return Response(RecipyGetSerializer(recipy).data)

    def destroy(self, request, id):
        recipy = get_object_or_404(Recipy, id=id)
        user = request.user
        favorite = get_object_or_404(
            Favorite, user=user, recipy=recipy
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateDesroyShopViewSet(CreateDestroyViewSet):
    """
    Вьюсет с двумя методами, создание и удаление.
    create: добавляет выбранный рецепт в список покупок,
    destroy: удаляет выбранный рецепт из списка покуок.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShoppingCartSerializer

    def create(self, request, id):
        user = request.user
        recipy = get_object_or_404(Recipy, id=id)
        ShoppingCart.objects.create(user=user, recipy=recipy)
        return Response(RecipyGetSerializer(recipy).data)

    def destroy(self, request, id):
        recipy = get_object_or_404(Recipy, id=id)
        user = request.user
        shopping_cart = get_object_or_404(
            ShoppingCart, user=user, recipy=recipy
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
