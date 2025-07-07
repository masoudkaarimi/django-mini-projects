from django.urls import path

from account.views import Auth

app_name = 'account'

urlpatterns = [
    path('register/', Auth.register_view, name='register'),
    path('login/', Auth.login_view, name='login'),
    path('logout/', Auth.logout_view, name='logout'),
    # path('dashboard/profile/password-change/', Auth.password_change_view, name='password_change'),
    # path('dashboard/profile/', Auth.profile_view, name='profile'),
]
