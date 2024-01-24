from django.urls import path
from . import views

urlpatterns = [
    path('get_income', views.build_funds_income),
    path('get_expense', views.build_funds_expense),
    path('get_transaction', views.build_funds_transaction),
]
