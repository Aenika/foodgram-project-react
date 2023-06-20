from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CreateDesroyFavViewSet,
    CreateDesroyShopViewSet,
    IngredientViewSet,
    RecipyViewSet,
    TagViewSet
)

v1_router = SimpleRouter()
v1_router.register('ingredients', IngredientViewSet)
v1_router.register('tags', TagViewSet)
v1_router.register('recipes', RecipyViewSet)

urlpatterns = [
    path('recipes/<int:id>/favorite/', CreateDesroyFavViewSet.as_view({
        'delete': 'destroy',
        'post': 'create'
    })),
    path('recipes/<int:id>/shopping_cart/', CreateDesroyShopViewSet.as_view({
        'delete': 'destroy',
        'post': 'create'
    })),
    path('', include(v1_router.urls)),
]
