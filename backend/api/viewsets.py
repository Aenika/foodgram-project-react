from rest_framework import mixins, viewsets


class CreateDestroyListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Создает вьюсет с тремя методами: вернуть список, удалить и создать"""
    pass
