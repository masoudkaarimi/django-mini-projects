from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from .views import register_view, login_view, logout_view, profile_view, password_change_view

app_name = 'account'

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/profile/", profile_view, name="profile"),
    path("password-change/", password_change_view, name="password-change"),
    path("password-change/done/", password_change_view, name="password-change-done"),
]
