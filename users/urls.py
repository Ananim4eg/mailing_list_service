from users.apps import UsersConfig
from users.views import RegisterView, CustomLoginView, CustomLogoutView, UserProfileView, UserUpdateProfileView, \
    ServiceUsersListView
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>', UserUpdateProfileView.as_view(), name='update_profile'),
    path('users/', ServiceUsersListView.as_view(), name='service_users'),
]
