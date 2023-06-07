from rest_framework import mixins, viewsets


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Создает вьюсет с двумя методами: создать и удалить"""
    pass
