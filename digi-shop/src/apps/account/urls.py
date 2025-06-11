from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from apps.account import views
from apps.account.forms import PasswordResetForm, SetPasswordForm

app_name = 'account'
urlpatterns = [
    path("password-reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset/confirm/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/activate/<slug:uidb64>/<slug:token>/', views.account_activate_view, name='account_activate'),

    path('account/profile', views.profile_view, name='profile'),
    path('account/profile/update/', views.profile_update_view, name='profile_update'),
    path('account/profile/update/avatar/', views.profile_update_avatar_view, name='profile_update_avatar'),
    path('account/profile/update/password/', views.profile_update_password_view, name='profile_update_password'),
    path('account/profile/delete/', views.profile_delete_view, name='profile_delete'),
    path('account/addresses', views.address_list_view, name='address_list'),
    path('account/addresses/<int:pk>/', views.address_detail_view, name='address_detail'),
    path('account/addresses/create/', views.address_create_view, name='address_create'),
    path('account/addresses/update/<int:pk>/', views.address_update_view, name='address_update'),
    path('account/addresses/set-default/<int:pk>/', views.address_set_default_view, name='address_set_default'),
    path('account/addresses/delete/<int:pk>/', views.address_delete_view, name='address_delete'),
    path('account/payments', views.payments_view, name='payments'),
    path('account/orders', views.orders_view, name='orders'),
    path('account/orders/<slug:order_slug>/', views.order_detail_view, name='order_detail'),
    path('account/', views.dashboard_view, name='dashboard'),
]
