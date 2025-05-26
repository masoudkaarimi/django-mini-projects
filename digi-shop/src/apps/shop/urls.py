from django.urls import path

from apps.shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_archive, name='product_archive'),
]
