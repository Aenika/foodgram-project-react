# flake8: noqa: I001, I004
from django.db import transaction
from django.http import HttpResponse
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
from .service import create_content


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
    filter_backends = [DjangoFilterBackend,]
    filterset_class = RecipyFilter
    serializer_class = RecipyGetSerializer

    def get_serializer_class(self):
        """Выбирает необходимый сериалайзер для действия."""
        if self.action == 'list' or self.action == 'retrieve':
            return RecipyGetSerializer
        return RecipySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Создаёт новый рецепт и М2М поля ингредиенты, теги для него."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().create(request, *args, **kwargs)
        instance = response.data
        recipy = Recipy.objects.get(id=instance['id'])
        return Response(RecipyGetSerializer(recipy).data)

    def update(self, request, *args, **kwargs):
        """Обновляет существующий рецепт и М2М поля ингредиенты, теги для него."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().update(request, *args, **kwargs)
        instance = response.data
        recipy = Recipy.objects.get(id=instance['id'])
        return Response(RecipyGetSerializer(recipy).data)

    @action(detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        """
        Формирует скачиваемый pdf файл со списком ингредентов и дозировкой
        для выбранных в "список покупок" рецептов.
        """
        user = request.user
        content = create_content(user)
        headers = {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="shopping_cart.pdf"',
        }
        return HttpResponse(
            content,
            headers=headers
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
    filter_backends = [DjangoFilterBackend,]
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
