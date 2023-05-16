from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('recipy/<int:pk>/', views.recipy_detail),
    path('new_recipy/', views.create_recipy, name='new_recipy'),
    path('search/', views.search)
]
