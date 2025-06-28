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

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('account/activate/<slug:uidb64>/<slug:token>/', views.AccountActivateView.as_view(), name='activate'),

    path('account/profile', views.ProfileView.as_view(), name='profile'),
    path('account/profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('account/profile/update/avatar/', views.ProfileAvatarUpdateView.as_view(), name='profile_update_avatar'),
    path('account/profile/update/password/', views.ProfileUpdatePasswordView.as_view(), name='profile_update_password'),
    path('account/profile/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),

    path('account/wishlist/', views.WishlistView.as_view(), name='wishlist'),

    path('account/address', views.AddressListView.as_view(), name='address_list'),
    path('account/address/<int:pk>/', views.AddressDeleteView.as_view(), name='address_detail'),
    path('account/address/create/', views.AddressCreateView.as_view(), name='address_create'),
    path('account/address/update/<int:pk>/', views.AddressUpdateView.as_view(), name='address_update'),
    path('account/address/set-default/<int:pk>/', views.AddressSetDefaultView.as_view(), name='address_set_default'),
    path('account/address/delete/<int:pk>/', views.AddressDetailView.as_view(), name='address_delete'),

    path('account/order', views.OrderListView.as_view(), name='order_list'),
    path('account/order/<slug:order_slug>/', views.OrderDetailView.as_view(), name='order_detail'),

    path('account/payment', views.PaymentMethodListView.as_view(), name='payment_list'),

    path('account/', views.DashboardView.as_view(), name='dashboard'),
]
