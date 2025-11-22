from users.apps import UsersConfig
from users.views import RegisterView
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
]