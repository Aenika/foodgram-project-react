from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from users.models import Follow

from .forms import RecipyForm
from .models import Recipy, Tag, User

recipes_per_page = 6


def paginising(recipes, recipes_per_page, request):
    paginator = Paginator(recipes, recipes_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@cache_page(120)
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
    tags = Recipy.objects.get(id=recipy_id).tags.all()
    context = {
        'recipy': recipy,
        'author': author,
        'tags': tags
    }
    return render(request, 'recipes/recipy_detail.html', context)


def search(request):
    keyword = request.GET.get('q')
    if keyword:
        recipes = Recipy.objects.select_related('author').filter(
            text__icontains=keyword
        )
    else:
        recipes = None
    context = {
        'recipes': recipes,
        'keyword': keyword,
    }

    return render(request, "recipes/search.html", context)


def search(request):
    keyword = request.GET.get("q", None)
    if keyword:
        recipes = Recipy.objects.select_related('author').filter(
            text__contains=keyword
        )
    else:
        recipes = None

    return render(
        request,
        "recipes/search.html",
        {"recipes": recipes,
         "keyword": keyword}
    )

# Recipy.objects.select_related('author').select_related('group').filter(text__contains=keyword).get()
# Запрос сделайте так, чтобы при обращении к свойствам модели author и group
# не порождались дополнительные запросы к базе.


def recipes_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    recipes = Recipy.objects.filter(tags__slug=slug)
    page_obj = paginising(recipes, recipes_per_page, request)
    context = {
        'tag': tag,
        'page_obj': page_obj
    }
    return render(request, "recipes/recipes_by_tag.html", context)


def profile(request, username):
    author = User.objects.get(username=username)
    recipes_by_author = Recipy.objects.select_related('author').filter(
        author=author
    )
    page_obj = paginising(recipes_by_author, recipes_per_page, request)
    following = (
        request.user.is_authenticated
        and request.user != author
        and Follow.objects.filter(user=request.user, author=author).exists()
    )
    reader = request.user
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following,
        'reader': reader
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


@login_required
def follow_index(request):
    recipes = Recipy.objects.select_related('author').filter(
        author__following__user=request.user
    )
    page_obj = paginising(recipes, recipes_per_page, request)
    context = {'page_obj': page_obj}
    return render(request, 'recipes/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    follower = request.user
    already_following = Follow.objects.filter(user=follower, author=author)
    if author != follower and not already_following.exists():
        Follow.objects.create(user=follower, author=author)
    return redirect('recipes:follow_index')


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follower = request.user
    already_following = Follow.objects.filter(user=follower, author=author)
    if already_following.exists():
        already_following.delete()
    return redirect('recipes:follow_index')
