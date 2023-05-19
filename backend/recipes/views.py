from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipyForm
from .models import Recipy, User

recipes_per_page = 6


def paginising(recipes, recipes_per_page, request):
    paginator = Paginator(recipes, recipes_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    recipes = Recipy.objects.order_by('-pub_date')
    page_obj = paginising(recipes, recipes_per_page, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'recipes/index.html', context)


@login_required
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


def recipy_detail(request, recipy_id):
    recipy = Recipy.objects.get(id=recipy_id)
    author = recipy.author
    context = {
        'recipy': recipy,
        'author': author,
    }
    return render(request, 'recipes/recipy_detail.html', context)


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


def profile(request, username):
    author = User.objects.get(username=username)
    recipes_by_author = Recipy.objects.select_related('author').filter(
        author=author
    )
    page_obj = paginising(recipes_by_author, recipes_per_page, request)
    context = {
        'author': author,
        'page_obj': page_obj
    }
    return render(request, 'recipes/profile.html', context)


@login_required
def recipy_edit(request, recipy_id):
    recipy = get_object_or_404(Recipy, id=recipy_id)
    form = RecipyForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipy
    )
    if request.user != recipy.author:
        return redirect('recipes:recipy_detail', recipy_id=recipy_id)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('recipes:recipy_detail', recipy_id=recipy_id)
    return render(request,
                  'recipes/new_recipy.html',
                  {
                      'form': form,
                      'is_edit': True
                  })