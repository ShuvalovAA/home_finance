from django.urls import path
from . import views

urlpatterns = [
    path('predict_day_of_year/', views.predict_day_of_year)
]