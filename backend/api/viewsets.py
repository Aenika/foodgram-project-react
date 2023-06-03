from rest_framework import mixins, viewsets


class CreateDestroyListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Создает вьюсет с тремя методами: создать, удалить и вернуть список"""
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
