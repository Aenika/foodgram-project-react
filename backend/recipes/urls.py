from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'recipy/<int:recipy_id>/',
        views.recipy_detail,
        name='recipy_detail'
    ),
    path('new_recipy/', views.create_recipy, name='new_recipy'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path(
        'recipes/<int:recipy_id>/edit/',
        views.recipy_edit,
        name='recipy_edit'
    ),
    # path('search/', views.search, name='search')
]