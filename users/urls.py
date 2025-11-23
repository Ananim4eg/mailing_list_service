from users.apps import UsersConfig
from users.views import RegisterView, CustomLoginView, CustomLogoutView
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
