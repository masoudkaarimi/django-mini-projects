from django.urls import path

from apps.inventory import views

app_name = 'inventory'

urlpatterns = [
    # ... your existing URLs
    path('api/products/variant/<int:variant_id>/', views.variant_json, name='variant_json'),
]