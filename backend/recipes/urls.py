from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('recipy/<int:pk>/', views.recipy_detail),
]
