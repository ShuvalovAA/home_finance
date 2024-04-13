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
from user import views

urlpatterns = [
    path('', views.render_profile_page),
    path('confirm_email/<auth_token>', views.confirm_email),
    path('signin/confirm_sms/', views.confirm_sms),
    path('signup/confirm_sms/', views.confirm_sms),
    path('signin/', views.sign_in, name='login'),
    path('signout/', views.sign_out, name='logout'),
    path('signup/', views.sign_up, name='register'),
    path('update/', views.update),
    path('get/', views.get),
    #заглушка для теста сервиса банка
    path('fixtures/bank_source', views.bank_source)
]
