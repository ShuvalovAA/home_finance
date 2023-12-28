import json

from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.timezone import localtime, now
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import ConfirmSMS, LoginForm, RegisterForm
from .handlers import confirm_login, confirm_phone, create_email_confirm, create_sms_confirm
from .models import User


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


def confirm_email(request, auth_token):
    """Подветредить адрес электронный почты."""
    breakpoint()
    try:
        user = User.objects.filter(auth_token=auth_token).first()
    except User.DoesNotExist as error:
        return HttpResponse({'Error': error.__str__()}, status=status.HTTP_404_NOT_FOUND)

    user.is_email_confirm = True
    user.save()
    return redirect('/swagger/')


def confirm_sms(request):
    """Подтверждение по смс."""
    if request.method != 'POST':
        redirect('/user/sigin/')
    if request.method == 'POST':
        form = ConfirmSMS(request.POST)
        if not form.is_valid():
            return HttpResponse(json.dumps(form.errors), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        code = int(form.cleaned_data['code'])
        user_id = int(form.cleaned_data['user_id'])
        register = int(form.cleaned_data['register'])

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as error:
            return HttpResponse({'Error': error.__str__()}, status=status.HTTP_404_NOT_FOUND)

        if register:
            try:
                confirm_phone(user=user, code=code)
            except Exception as error:
                return HttpResponse({'Error': error.__str__()}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            try:
                confirm_login(user=user, code=code)
            except Exception as error:
                return HttpResponse({'Error': error.__str__()}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        login(request, user)
        return redirect('/swagger/')


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
            create_email_confirm(user)
            create_sms_confirm(user)
            return render(
                request=request,
                template_name='confirm_sms.html',
                context={'user_id': user.id, 'register': 1}
            )
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
                create_sms_confirm(user)
                if user.is_phone_confirm:
                    return render(
                        request=request,
                        template_name='confirm_sms.html',
                        context={'user_id': user.id, 'register': 0}
                    )
                else:
                    return render(
                        request=request,
                        template_name='confirm_sms.html',
                        context={'user_id': user.id, 'register': 1}
                    )
        return HttpResponse(json.dumps(form.errors), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


def sign_out(request):
    """Провести деавторизацию пользователя."""
    logout(request)
    return redirect('/user/signin/')
