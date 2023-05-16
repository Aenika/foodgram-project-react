from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RecipyForm
from .models import Recipy


def index(request):
    recipes = Recipy.objects.order_by('-pub_date')[:10]
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)


def create_recipy(request):
    if request.method == 'POST':
        form = RecipyForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            user = request.user
            form.instance.author = user
            form.save()
            return redirect('recipes:index')
        return render(request, 'recipes/new_recipy.html', {'form': form})
    form = RecipyForm()
    return render(request, 'recipes/new_recipy.html', {'form': form})


def recipy_detail(request, pk):
    return HttpResponse(f'Рецебд номер {pk}')


def search(request):
    keyword = request.GET.get("q", None)
    if keyword:
        posts = Recipy.objects.filter(text__contains=keyword).get()
    else:
        posts = None

    return render(request, "index.html", {"posts": posts, "keyword": keyword})

# Recipy.objects.select_related('author').select_related('group').filter(text__contains=keyword).get()
# Запрос сделайте так, чтобы при обращении к свойствам модели author и group
# не порождались дополнительные запросы к базе.
