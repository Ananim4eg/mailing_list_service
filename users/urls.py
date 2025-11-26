from users.apps import UsersConfig
from users.views import RegisterView, CustomLoginView, CustomLogoutView, UserProfileView, UserUpdateProfileView, \
    ServiceUsersListView, ActivateView, CustomPasswordResetView, CustomPasswordResetConfirmView
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>', UserUpdateProfileView.as_view(), name='update_profile'),
    path('users/', ServiceUsersListView.as_view(), name='service_users'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_confirm'),
]
