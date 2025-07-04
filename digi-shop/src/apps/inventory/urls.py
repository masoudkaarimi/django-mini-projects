from django.urls import path, re_path

from apps.inventory import views

app_name = 'inventory'

urlpatterns = [
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    re_path(r'^category/(?P<path>.+)/$', views.CategoryProductListView.as_view(), name='category_detail'),
    path('brand/', views.BrandListView.as_view(), name='brand_list'),
    path('brand/<slug:slug>/', views.BrandProductListView.as_view(), name='brand_detail'),
]
