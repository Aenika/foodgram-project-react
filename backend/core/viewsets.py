from rest_framework import mixins, viewsets


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Создает вьюсет с двумя методами: создать и удалить.
    Для подписок в приложении users и списка покупок
    и избранного в приложении api.
    """
    pass
