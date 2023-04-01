from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('recipes.urls', namespace='recipes')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
]
