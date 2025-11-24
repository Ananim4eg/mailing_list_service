from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import FormView, DetailView, UpdateView, ListView

from users.forms import CustomUserCreateForm, CustomUserLogin, ProfileForm
from users.models import CustomUser


class RegisterView(FormView):
    """Контроллер формы регистрации"""
    form_class = CustomUserCreateForm
    template_name = 'registration.html'
    success_url = reverse_lazy('mailing:home_page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


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
    context_object_name = 'user'


class UserUpdateProfileView(UpdateView):
    """Контроллер для профиля пользователя"""

    model = CustomUser
    form_class = ProfileForm
    template_name = 'update_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Получаем текущего пользователя и пользователя для профиля и передаем в шаблон"""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['service_user'] = get_object_or_404(CustomUser, pk=self.kwargs['pk'])

        return context

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})


class ServiceUsersListView(ListView):
    """Контроллер для списка пользователей"""

    model = CustomUser
    template_name = 'service_users.html'
    context_object_name = 'users'
