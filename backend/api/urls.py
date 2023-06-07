from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateDesroyFavViewSet, CreateDesroyFollowViewSet,
                    CreateDesroyShopViewSet, FollowViewSet, IngredientViewSet,
                    RecipyViewSet, TagViewSet)

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipyViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/subscriptions/',
        FollowViewSet.as_view()
    ),
    path(
        'users/<int:id>/subscribe/',
        CreateDesroyFollowViewSet.as_view(),
        name='subscribe'
    ),
    path('recipes/<int:id>/favorite/', CreateDesroyFavViewSet.as_view()),
    path('recipes/<int:id>/shopping_cart/', CreateDesroyShopViewSet.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
