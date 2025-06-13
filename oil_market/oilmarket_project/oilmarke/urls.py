from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('report/', views.transactions_report, name='transactions_report'),
    path('chart/', views.sales_chart, name='sales_chart'),
]