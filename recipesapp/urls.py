from django.urls import path
from .views import *

app_name = 'recipesapp'

urlpatterns = [
    path('', index_view, name='index'),
    path('about/', about_view, name='about'),
    path('search/', search, name='search'),
    path('create/', create_recipe, name='create_recipe'),
    path('recipes/', show_all_recipes, name='all_recipes'),
    path('recipes/<int:pk>', show_recipe_details, name='recipe_details'),
    path('category/<int:pk>', recipes_by_category, name='recipes_by_category'),
    path('author/<int:pk>', recipes_by_author, name='recipes_by_author'),
    path('recipes/<int:pk>/edit', edit_recipe, name='edit_recipe'),
    path('recipes/<int:pk>/delete', delete_recipe, name='delete_recipe'),
]