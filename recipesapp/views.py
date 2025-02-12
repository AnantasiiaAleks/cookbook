import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm
from .models import Recipe, Category




# Create your views here.
def index_view(request):
    """
    Главная страница:
    Загрузка из БД всех рецептов, выбор из них случайного
    Загрузка из БД последних 6 рецептов
    Загрузка из БД категорий
    :param request: get
    :return: шаблон главной страницы.
    """
    all_recipes = Recipe.objects.all().only('title', 'description', 'photo')
    random_recipe = random.choice(all_recipes) if all_recipes else None
    last_recipes = (Recipe.objects.all() \
                        .order_by('-id')[:6] \
                        .only('title', 'description', 'photo'))
    categories = Category.objects.all()
    context = {'last_recipes': last_recipes,
               'categories': categories,
               'random_recipe': random_recipe
               }
    return render(request, 'index.html', context)


def about_view(request):
    """
    Страница about
    :param request: get
    :return: шаблон страницы about.
    """
    return render(request, 'about.html')

def search(request):
    """
    Поиск по названию рецепта (краткий вывод)
    :param request: get
    :return: шаблон списка рецептов с результатами поиска.
    """
    search_query = request.GET.get('search_query', '').strip().lower()
    print(search_query)
    page = 'search_results'
    page_title = f'Поиск: {search_query}'
    results = Recipe.objects.filter(title_lower__icontains=search_query).only('title', 'description', 'photo')
    context = {
        'page': page,
        'page_title': page_title,
        'search_query': search_query,
        'results': results
    }
    return render(request, 'recipesapp/recipes_list.html', context)


def show_all_recipes(request):
    """
    Список всех рецептов из БД (краткий вывод)
    :param request: get
    :return: шаблон списка рецептов (все рецепты из БД).
    """
    page = 'all_recipes'
    page_title = 'Все рецепты'
    all_recipes = Recipe.objects.all().only('title', 'description', 'photo')
    context = {
        'page': page,
        'page_title': page_title,
        'all_recipes': all_recipes
    }
    return render(request, 'recipesapp/recipes_list.html', context)


def recipes_by_category(request, pk):
    """
    Список рецептов конкретной категории (краткий вывод)
    :param request: get
    :param pk: pk категории
    :return: шаблон списка рецептов (рецепты конкретной категории).
    """
    page = 'recipes_by_category'
    category = get_object_or_404(Category, pk=pk)
    page_title = f'Категория: {category.name}'
    recipes_by_category = Recipe.objects.filter(category=category).only('title', 'description', 'photo')
    context = {
        'page': page,
        'page_title': page_title,
        'recipes_by_category': recipes_by_category
    }
    return render(request, 'recipesapp/recipes_list.html', context)

def recipes_by_author(request, pk):
    """
    Список рецептов конкретного автора (зарегистрированного пользователя) (краткий вывод)
    :param request: get
    :param pk: pk зарегистрированного пользователя
    :return: шаблон списка рецептов (рецепты авторства конкретного пользователя).
    """
    page = 'recipes_by_author'
    author = get_object_or_404(User, pk=pk)
    page_title = f'Автор: {author.username}'
    recipes_by_author = Recipe.objects.filter(author=author).only('title', 'description', 'photo')
    context = {
        'page': page,
        'page_title': page_title,
        'recipes_by_author': recipes_by_author
    }
    return render(request, 'recipesapp/recipes_list.html', context)


def show_recipe_details(request, pk):
    """
    Детальная информация по конкретному рецепту
    :param request: get
    :param pk: pk рецепта
    :return: шаблон детального описания рецепта.
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredient_list = recipe.ingredients.split('\n')
    step_list = recipe.cooking_steps.split('\n')
    context = {
        'recipe': recipe,
        'ingredient_list': ingredient_list,
        'step_list': step_list
    }
    return render(request, 'recipesapp/recipe_details.html', context)


@login_required
def create_recipe(request):
    """
    Доступно авторизованному пользователю.
    Страница создания записи рецепта
    :param request: get и post
    :return: шаблон формы создания и сохранения рецепта.
    """
    current_user = request.user
    categories = Category.objects.all()
    recipe_form = RecipeForm()
    recipe_form.fields['category'].queryset = categories
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = current_user
            recipe.save()
            return redirect('usersapp:profile')
    return render(request, 'recipesapp/recipe_form.html', {'recipe_form': recipe_form, 'categories': categories})


@login_required
def show_my_recipes(request):
    """
    Доступно авторизованному пользователю.
    Страница с перечнем рецептов, сохраненных текущим пользователем (краткий вывод). Доступно на странице профиля.
    :param request: get
    :return: шаблон списка рецептов (рецепты авторства текущего пользователя)
    """
    current_user = request.user
    user_recipes = Recipe.objects.filter(author=current_user).only('title', 'description', 'photo')
    return render(request, 'recipesapp/recipes_list.html', {'recipes_list': user_recipes})


@login_required
def edit_recipe(request, pk):
    """
    Доступно авторизованному пользователю.
    Страница внесения изменений в рецепт.
    :param request: get и post
    :param pk: pk рецепта
    :return: шаблон формы создания и сохранения рецепта.
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if recipe_form.is_valid():
            recipe_form.save()
            return redirect('recipesapp:recipe_details', pk=recipe.pk)
    else:
        recipe_form = RecipeForm(instance=recipe)

    context = {
        'recipe_form': recipe_form,
        'recipe': recipe,
        'categories': categories,
    }
    return render(request, 'recipesapp/recipe_form.html', context)


@login_required
def delete_recipe(request, pk):
    """
    Доступно авторизованному пользователю.
    Страница удаления рецепта.
    :param request: get и post
    :param pk: pk рецепта
    :return: шаблон с информацией об успешном удалении рецепта.
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author == request.user:
        if request.method == 'POST':
            recipe.delete()
            return redirect('usersapp:profile')

        return render(request, 'recipesapp/delete_recipe.html', {'recipe': recipe})
