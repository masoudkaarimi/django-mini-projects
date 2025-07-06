from django.urls import path

from loan.views import dashboard_view, loan_list_view, loan_detail_view, loan_create_view, loan_update_view, loan_delete_view, user_list_view, user_detail_view, user_create_view, \
    user_update_view, user_delete_view, loan_installment_payment_view

app_name = "loan"

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),

    path('dashboard/loans/list/', loan_list_view, name='loan_list'),
    path('dashboard/loans/<int:pk>/', loan_detail_view, name='loan_detail'),
    path('dashboard/loans/create/', loan_create_view, name='loan_create'),
    path('dashboard/loans/<int:pk>/edit/', loan_update_view, name='loan_edit'),
    path('dashboard/loans/delete/', loan_delete_view, name='loan_delete'),
    path('dashboard/loans/installments/payment/', loan_installment_payment_view, name='loan_installment_payment'),

    path('dashboard/users/list/', user_list_view, name='user_list'),
    path('dashboard/users/<int:pk>/', user_detail_view, name='user_detail'),
    path('dashboard/users/create/', user_create_view, name='user_create'),
    path('dashboard/users/<int:pk>/edit/', user_update_view, name='user_edit'),
    path('dashboard/users/delete/', user_delete_view, name='user_delete'),
]
