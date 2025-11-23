from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import FormView, DetailView

from users.forms import CustomUserCreateForm, CustomUserLogin
from users.models import CustomUser


class RegisterView(FormView):
    """Контроллер формы регистрации"""
    form_class = CustomUserCreateForm
    template_name = 'registration.html'
    success_url = reverse_lazy('mailing:home_page')


class CustomLoginView(LoginView):
    """Контроллер формы авторизации"""
    form_class = CustomUserLogin
    template_name = 'login.html'


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):

        logout(request)

        messages.info(request, 'Вы успешно вышли из системы.')

        return redirect('mailing:home_page')


class UserProfileView(DetailView):
    """Контроллер для профиля пользователя"""

    model = CustomUser
    template_name = 'profile.html'
