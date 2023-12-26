from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.shortcuts import redirect, render
from django.utils.timezone import localtime, now
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import json

from .forms import LoginForm, RegisterForm
from .models import User
from .handlers import create_sms_confirm


@swagger_auto_schema(method='PATCH', tags=['User'])
@api_view(['PATCH'])
def update(request):
    """Обновить данные пользователя."""
    pass


@swagger_auto_schema(method='GET', tags=['User'])
@api_view(['GET'])
def get(request):
    """Получить данные пользователя."""
    user = User.objects.get(pk=request.GET['id'])
    user_dict = model_to_dict(user)
    return Response(user_dict, status=status.HTTP_200_OK)


def sign_up(request):
    """Провести регистрацию нового пользователя."""
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('register_ok')
            user = form.save(commit=False)
            user.username = user.phone
            user.register_date = localtime(now())
            user.is_active = True
            user.is_service_account = False
            user.save()
            user = authenticate(
                request=request,
                username=user.username,
                password=request.POST.get('password1')
            )
            breakpoint()
            create_sms_confirm(user)
            login(request, user)
            return redirect('/swagger/')
        else:
            return render(request, 'signup.html', {'form': form})


def sign_in(request):
    """Провести авторизацию пользователя."""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'signin.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/swagger/')
        return HttpResponse(json.dumps(form.errors), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


def sign_out(request):
    """Провести деавторизацию пользователя."""
    logout(request)
    return redirect('/user/login/')
