from django.urls import path

from apps.checkout import views

app_name = 'checkout'

urlpatterns = [
    # Main cart page
    path('cart/', views.CartView.as_view(), name='cart'),

    # AJAX endpoints
    path('cart/add/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/', views.UpdateCartItemView.as_view(), name='update_cart'),
    path('cart/remove/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/clear/', views.ClearCartView.as_view(), name='clear_cart'),
    path('cart/sync/', views.SyncCartView.as_view(), name='sync_cart'),
    path('cart/check-inventory/<int:product_variant_id>/', views.CheckInventoryView.as_view(), name='check_inventory'),


]
