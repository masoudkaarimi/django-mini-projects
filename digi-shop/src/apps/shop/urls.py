from django.urls import path

from apps.shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_archive, name='product_archive'),
    path('categories/', views.category_archive, name='category_archive'),
    path('categories/<slug:category_slug>/', views.category_single, name='category_single'),
    path('brands/', views.brand_archive, name='brand_archive'),
    path('brands/<slug:brand_slug>/', views.brand_single, name='brand_single'),
]
