# flake8: noqa: I001, I004
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (Dosage, Favorite, Ingredient, Recipy, ShoppingCart,
                            Tag)
from users.models import Follow, User

from .filters import RecipyByTagSlugFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipesShort,
                          RecipyGetSerializer, RecipySerializer, TagSerializer,
                          UserRecipesSerializer)


class RecipyViewSet(viewsets.ModelViewSet):
    queryset = Recipy.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipyByTagSlugFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipyGetSerializer
        return RecipySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().create(request, *args, **kwargs)
        instance = response.data
        recipy = Recipy.objects.get(id=instance['id'])
        return Response(RecipyGetSerializer(recipy).data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().update(request, *args, **kwargs)
        instance = response.data
        recipy = Recipy.objects.get(id=instance['id'])
        return Response(RecipyGetSerializer(recipy).data)

    @action(detail=False, url_path='shopping_cart')
    def shopping_cart(self, request):
        user = request.user
        recipes = Recipy.objects.filter(recipes_shoppingcarts__user=user)
        serializer = RecipesShort(recipes, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='favorite')
    def favorite(self, request):
        user = request.user
        recipes = Recipy.objects.filter(recipes_favorites__user=user)
        serializer = RecipesShort(recipes, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = Dosage.objects.filter(
            recipy__recipes_shoppingcarts__user=user
        ).values('ingredient').annotate(sum_amount=Sum('amount'))
        content = 'Необходимо купить: \n'
        for i in ingredients:
            ingredient = get_object_or_404(Ingredient, id=i['ingredient'])
            amount = i['sum_amount']
            content += (
                f'- {ingredient.name}'
                f' ({ingredient.measurement_unit})'
                f' — {amount};\n'
            )
        content += (
            '\n Спасибо, что воспользовались приложением от Вики'
            '\n https://github.com/Aenika'
        )
        headers = {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="shopping_cart.pdf"',
        }
        return HttpResponse(
            content,
            headers=headers
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class FollowViewSet(
    generics.ListAPIView
):
    serializer_class = UserRecipesSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(follower__user=current_user)


class CreateDesroyFollowViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return HttpResponse(400, 'На себя нельзя подписываться')
        if Follow.objects.filter(user=user, author=author).exists():
            return HttpResponse(400, 'Подписка уже существует')
        Follow.objects.create(user=user, author=author)
        return Response(UserRecipesSerializer(author).data)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        user = request.user
        follow = get_object_or_404(
            Follow, user=user, author=author
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateDesroyFavViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        user = request.user
        recipy = get_object_or_404(Recipy, id=id)
        if Favorite.objects.filter(user=user, recipy=recipy).exists():
            return HttpResponse(400, 'Уже в списке избранного')
        Favorite.objects.create(user=user, recipy=recipy)
        return Response(RecipesShort(recipy).data)

    def delete(self, request, id):
        recipy = get_object_or_404(Recipy, id=id)
        user = request.user
        favorited = get_object_or_404(
            Favorite, user=user, recipy=recipy
        )
        favorited.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateDesroyShopViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        user = request.user
        recipy = get_object_or_404(Recipy, id=id)
        if ShoppingCart.objects.filter(user=user, recipy=recipy).exists():
            return HttpResponse(400, 'Уже в списке избранного')
        ShoppingCart.objects.create(user=user, recipy=recipy)
        return Response(RecipesShort(recipy).data)

    def delete(self, request, id):
        recipy = get_object_or_404(Recipy, id=id)
        user = request.user
        in_cart = get_object_or_404(
            ShoppingCart, user=user, recipy=recipy
        )
        in_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
