from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import CustomUserCreateForm


class RegisterView(FormView):
    form_class = CustomUserCreateForm
    template_name = 'registration.html'
    success_url = reverse_lazy('mailing:home_page')
