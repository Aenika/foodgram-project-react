# flake8: noqa: I001, I005
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CreateDesroyFavViewSet,
    CreateDesroyShopViewSet,
    IngredientViewSet,
    RecipyViewSet,
    TagViewSet
)

v1_router = DefaultRouter()
v1_router.register('ingredients', IngredientViewSet, basename='ingredients')
v1_router.register('recipes', RecipyViewSet, basename='recipes')
v1_router.register('tags', TagViewSet, basename='tags')

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
