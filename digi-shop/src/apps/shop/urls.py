from django.urls import path

from apps.shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
]
