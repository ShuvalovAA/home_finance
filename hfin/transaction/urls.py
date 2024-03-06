"""
URL configuration for hfin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from transaction import views

urlpatterns = [
    path('', views.render_transaction_page),
    path('create/', views.create),
    path('update/', views.update),
    path('delete/', views.delete),
    path('copy/', views.copy),
    path('get/', views.get),
    path('delete/bulk/', views.delete_bulk),
    path('get/bulk/', views.get_bulk),
    path('copy/bulk/', views.copy_bulk),
    path('update/bulk/', views.update_bulk),
    path('get_count_for_paggination/', views.get_count_for_paggination)
]
