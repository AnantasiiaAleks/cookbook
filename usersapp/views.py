from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from recipesapp.models import Recipe

from .forms import CustomUserCreationForm

# Create your views here.
def login_view(request):
    """
    Страница и форма авторизации пользователя.
    :param request: get и post
    :return: шаблон авторизации и регистрации пользователя.
    """
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Введите имя пользователя и пароль!')
            return render(request, 'usersapp/login_register.html', {'page': 'login'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'usersapp:profile'))
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'usersapp/login_register.html', {'page': 'login'})

@login_required
def logout_view(request):
    """
    Доступно авторизованному пользователю.
    Представление выхода пользователя из системы.
    :param request: get
    :return: редирект на главную страницу со статусом "неавторизован".
    """
    logout(request)
    messages.info(request, 'До новых встреч!')
    return redirect('recipesapp:index')


def register_view(request):
    """
    Страница регистрации пользователя
    :param request: get и post
    :return: шаблон регистрации пользователя в системе.
    """
    page = 'register'
    register_form = CustomUserCreationForm()

    if request.method == 'POST':
        register_form = CustomUserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            messages.success(request, 'Персональная кулинарная книга создана. Добро пожаловать!')
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Возникла ошибка, попробуйте еще раз')

    context = {'page': page, 'register_form': register_form}
    return render(request, 'usersapp/login_register.html', context)


@login_required
def profile_view(request):
    """
    Доступно авторизованному пользователю.
    Страница профиля авторизованного пользователя.
    На странице подгружается список сохраненных текущим пользователем рецептов.
    :param request: get
    :return: шаблон авторизованного профиля пользователя.
    """
    name = request.user.first_name or request.user.username
    user_id = request.user.pk
    profile_recipes = Recipe.objects.filter(author=user_id).only('title', 'description', 'photo')
    context = {
        'name': name,
        'profile_recipes': profile_recipes
    }
    return render(request, 'usersapp/profile.html', context)