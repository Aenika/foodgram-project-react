from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    template = 'recipes/index.html'
    return render(request, template)


def recipy_detail(request, pk):
    return HttpResponse(f'Рецебд номер {pk}')
