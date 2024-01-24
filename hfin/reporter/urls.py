from django.urls import path
from . import views

urlpatterns = [
    path('get_income', views.get_income),
    path('get_expense', views.get_expense),
    path('get_transaction', views.get_transaction),
]
