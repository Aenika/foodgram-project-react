from django.http import HttpResponse
from django.shortcuts import render

from .models import Recipy


def index(request):
    recipes = Recipy.objects.order_by('-pub_date')[:10]
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)


def recipy_detail(request, pk):
    return HttpResponse(f'Рецебд номер {pk}')
