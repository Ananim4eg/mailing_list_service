from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views.generic import DetailView, UpdateView, ListView

from users.forms import CustomUserCreateForm, CustomUserLogin, ProfileForm
from users.models import CustomUser
from users.tokens import email_confirm_token


class RegisterView(View):
    """Контроллер формы регистрации"""
    template_name = 'registration.html'

    def get(self, request):
        form = CustomUserCreateForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Подтвердите ваш email'
            message = render_to_string('emails/confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_confirm_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            messages.success(request, 'Проверьте почту для подтверждения регистрации.')
            return redirect('users:login')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    """Контроллер формы авторизации"""
    form_class = CustomUserLogin
    template_name = 'login.html'


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):

        logout(request)

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

    def get_object(self, queryset = None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            return self.object
        raise PermissionDenied('Этот профиль другого пользователя')

    def get_form(self, form_class=None):
        """Формируем поля формы в зависимости от прав пользователя"""
        form = super().get_form(form_class)

        form_fields = ['email', 'avatar', 'phone_number', 'country',]

        if self.request.user.groups.filter(name='manager').exists() and self.request.user.pk != self.object.pk:
            for field in form_fields:
                form.fields.pop(field, None)

        if self.object.is_superuser:
            raise PermissionDenied("Вы не можете изменять профиль суперпользователя")

        return form

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})


class ServiceUsersListView(ListView):
    """Контроллер для списка пользователей"""

    model = CustomUser
    template_name = 'service_users.html'
    context_object_name = 'users'


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and email_confirm_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Ваш аккаунт активирован! Теперь вы можете войти.')
            return redirect('users:login')
        else:
            messages.error(request, 'Ссылка активации недействительна.')
            return redirect('users:registration')
