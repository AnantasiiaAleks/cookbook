from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError



class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя
    """
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean_username(self):
        """
        Валидация имени пользователя
        :return: username
        """
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError("Такой пользователь уже есть")
        return username

    def clean_email(self):
        """
        Валидация адреса электронной почты
        :return: email
        """
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def password2_clean(self):
        """
        Валидация паролей, в т.ч. совпадения повтора пароля
        :return: password2
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        """
        Сохранение пользователя в БД
        :param commit:
        :return: user
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



