import os
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .utilites import translit

# Create your models here.
class Category(models.Model):
    """
    Модель категории.

    :param name: Наименование категории.
    :param picture: Картинка для категории.
    """
    name = models.CharField('Категория', max_length=50)
    picture = models.ImageField(upload_to="categories/")

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """
        :return: строковое представление категории
        """
        return self.name


class Recipe(models.Model):
    """
    Модель рецепта.

    :param title: Название рецепта.
    :param title_lower: Название рецепта строчными буквами.
    :param description: Краткое описание рецепта.
    :param ingredients: Перечень ингредиентов.
    :param cooking_steps: Перечень этапов приготовления.
    :param cooking_time: Время приготовления.
    :param photo: Фотография или картинка блюда.
    :param author: Указание на автора рецепта (внешний ключ к модели пользователей).
    :param post_date: Дата публикации. Устанавливается автоматически.
    :param category: Категория блюда (внешний ключ к модели категорий).
    """
    title = models.CharField('Название', max_length=100)
    title_lower = models.CharField('Строчное название', max_length=100, null=True, blank=True)
    description = models.CharField('Описание', max_length=200)
    ingredients = models.TextField('Ингредиенты', default='Не указано')
    cooking_steps = models.TextField('Этапы приготовления')
    cooking_time = models.IntegerField('Время приготовления (минуты)')
    photo = models.ImageField(upload_to="recipes/", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    post_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категории', default=6)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """
        :return: строковое представление рецепта
        """
        return f'{self.author}: {self.title}'

    def get_absolute_url(self):
        """
        Динамическое формирование URL на основе pk объекта.
        :return: URL-адрес для конкретного рецепта
        """
        return reverse('recipe_details', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        Сохранение в БД рецепта.
        Формирование имени загружаемого пользователем изображения
        :param args:
        :param kwargs:
        """
        self.title_lower = self.title.lower() if self.title else None
        if self.category and self.title:
            category_name = translit(self.category.name)
            if self.photo:
                file_extension = os.path.splitext(self.photo.name)[1]
                translit_title = translit(self.title)
                new_file_name = f"{translit_title}{file_extension}"
                self.photo.name = f"{category_name}/{new_file_name}"
            else:
                if not self.pk:
                    self.photo = 'recipes/default_recipe.jpg'

        super().save(*args, **kwargs)

