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

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipyViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('recipes/<int:id>/favorite/', CreateDesroyFavViewSet.as_view({
            'delete': 'destroy',
            'post': 'create'
        })),
    path('recipes/<int:id>/shopping_cart/', CreateDesroyShopViewSet.as_view({
            'delete': 'destroy',
            'post': 'create'
        })),
    path('', include(router.urls)),
]
