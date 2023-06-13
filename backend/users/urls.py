from django.urls import include, path

from .views import CreateDesroyFollowViewSet, FollowViewSet

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/subscriptions/',
        FollowViewSet.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:id>/subscribe/',
        CreateDesroyFollowViewSet.as_view({
            'delete': 'destroy',
            'post': 'create'
        }),
        name='subscribe'
    ),
    path('', include('djoser.urls')),
]
