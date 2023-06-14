# flake8: noqa: I001, I004
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.pagination import CustomPagination
from core.viewsets import CreateDestroyViewSet
from .models import Follow, User
from .serializers import FollowSerializer, UserRecipesSerializer


class FollowViewSet(generics.ListAPIView):
    """Вьюсет для отображения списка подписок."""
    serializer_class = UserRecipesSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(follower__user=current_user)


class CreateDesroyFollowViewSet(CreateDestroyViewSet):
    """
    Вьюсет с двумя методами, создание и удаление.
    create: добавляет выбранного автора в список подписок,
    destroy: удаляет выбранного автора из списка подписок.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer

    def create(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        Follow.objects.create(user=user, author=author)
        return Response(UserRecipesSerializer(author).data)

    def destroy(self, request, id):
        author = get_object_or_404(User, id=id)
        user = request.user
        follow = get_object_or_404(
            Follow, user=user, author=author
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
