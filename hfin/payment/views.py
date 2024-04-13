from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from root.decorators import check_premission
from .serializers import SendSerializer, GetSerializer, GetByUserSerializer
from clients.payment_handler import payment_handler
from user.models import User
from .models import Tariff, UsersPayments
from django.shortcuts import redirect
import json
from datetime import datetime


@swagger_auto_schema(method='GET', query_serializer=SendSerializer, tags=['Payments'])
@api_view(['GET'])
@check_premission
def send(request):
    """Отправить запрос на оплату."""
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    tariff_name = request.GET.get('tariff')
    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)
    try:
        tariff = Tariff.objects.get(name=tariff_name)
    except Tariff.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    target_url = payment_handler.send_payment(user=user, product=tariff, amount=tariff.price)
    return redirect(target_url)

@swagger_auto_schema(method='get', query_serializer=GetByUserSerializer, tags=['Payments'])
@api_view(['GET'])
@check_premission
def get(request):
    """Получить выборку по платежам пользователя."""
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    user_id = request.GET.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    UsersPayments.objects._using_default()
    payments = UsersPayments.objects.filter(user_id=user.id, done=True).order_by('date').values_list(
        'date__date',
        'tariff__price',
        'tariff__period_months'
    )
    if not payments:
        return Response(UsersPayments.DoesNotExist.__str__, status=status.HTTP_404_NOT_FOUND)

    return Response(payments, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', query_serializer=GetSerializer, tags=['Payments'])
@api_view(['GET'])
def webhook_get_pay(request):
    """Получить платёж."""
    # ТРЕБУЕТСЯ ПЕРЕДЕЛАТЬ
    # if not request.method == 'GET':
    #     return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    # # data = json.loads(request.GET.get('data'))
    # data = request.GET

    # try:
    #     user_id = data.get('user_id')
    #     user = User.objects.get(pk=user_id)
    #     # user = User.objects.get(pk=data.get('user_id'))
    # except User.DoesNotExist as error:
    #     return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)
    # name = data.get('good')
    # Tariff.objects._using_default()
    # tariff = Tariff.objects.filter(name=name).last()
    # # tariff = Tariff.objects.filter(period_months=data.get('product_name')).last()
    # params = {
    #     'user': user,
    #     'date': datetime.now(),
    #     'tariff': tariff,
    #     'done': True
    #     }
    # try:
    #     payment_handler.webhook_get_pay(params=params)
    # except UsersPayments.DoesNotExist as error:
    #     return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    return Response('', status=status.HTTP_200_OK)
