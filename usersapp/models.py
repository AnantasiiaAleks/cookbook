from django.db import models
from django.conf import settings


# Create your models here.
class Profile(models.Model):
    """
    Модель профиля пользователя.

    :param user: Авторизованный пользователь.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        """
        Строковое представление профиля пользователя.
        :return:
        """
        return f"{self.user.username}'s Profile"