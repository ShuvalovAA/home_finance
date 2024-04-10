from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_reporter_page),
    path('get_income', views.get_income),
    path('get_expense', views.get_expense),
    path('get_transaction', views.get_transaction),
    path('by_group/get_income', views.get_grouping_income),
    path('by_group/get_expense', views.get_grouping_expense)
]
