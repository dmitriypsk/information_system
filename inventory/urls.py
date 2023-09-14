from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('new/', views.product_create, name='product_create'),
    path('edit/<int:pk>/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/new/', views.transaction_create, name='transaction_create'),
    path('transactions/return/create/', views.transaction_return_create, name='transaction_return_create'),
    path('report/', views.report, name='report'),
    path('report/export/', views.export_report_to_excel, name='export_report_to_excel'),
    path('credit_sales/', views.credit_sales_list, name='credit_sales_list'),
    path('credit_sales/new/', views.credit_sale_create, name='credit_sale_create'),
    path('credit_sales/<int:credit_sale_id>/payments/', views.credit_payments_list, name='credit_payments_list'),
    path('credit_sales/<int:credit_sale_id>/payments/new/', views.credit_payment_create, name='credit_payment_create'),
    path('settled_credits/', views.settled_credits, name='settled_credits'),
    path('unsettled_credits/', views.unsettled_credits, name='unsettled_credits'),
    path('credit_return/<int:credit_sale_id>/', views.credit_return, name='credit_return'),
    path('inventory/credit_sales/payments/<int:credit_payment_id>/toggle_paid/', views.credit_payment_toggle_paid, name='credit_payment_toggle_paid'),
    path('credit_payment_create/<int:credit_sale_id>/', views.credit_payment_create, name='credit_payment_create'),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/inventory/login/'), name='logout'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
]