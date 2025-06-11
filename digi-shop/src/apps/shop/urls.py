from django.urls import path

from apps.shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_archive_view, name='product_archive'),
    path('products/<slug:product_slug>/', views.product_single_view, name='product_single'),
    path('categories/', views.category_archive_view, name='category_archive'),
    path('categories/<slug:category_slug>/', views.category_single_view, name='category_single'),
    path('brands/', views.brand_archive_view, name='brand_archive'),
    path('brands/<slug:brand_slug>/', views.brand_single_view, name='brand_single'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]
