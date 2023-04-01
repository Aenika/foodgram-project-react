from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index),
    path('recipy/<int:pk>/', views.recipy_detail),
]
