import json
import datetime
import math
import csv
import os
from django.forms.models import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from transaction.models import Transaction
from expense.models import Expense
from rest_framework import parsers, renderers, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from root.decorators import check_premission, is_authenticated_and_is_active
from root.settings import MEDIA_URL
from django.shortcuts import render
from user.models import User
from transaction.handlers import DownloadDirector


from .serializers import (
    CopyTransactionBulkSerializer,
    CopyTransactionSerializer,
    CreateTransactionSerializer,
    DeleteTransactionBulkSerializer,
    DeleteTransactionSerializer,
    CountTransactionSerializer,
    GetTransactionBulkSerializer,
    GetTransactionSerializer,
    UpdateTransactionBulkSerializer,
    UpdateTransactionSerializer,
    DownloadFileSerializer,
    TransactionDataSerializer
)


@is_authenticated_and_is_active
def render_transaction_page(request):
    """Рендер на страницу транзакций."""
    return render(request, 'transaction.html')


@swagger_auto_schema(method='GET', query_serializer=CountTransactionSerializer, tags=['transaction'])
@api_view(['GET'])
@check_premission
def get_count_for_paggination(request):
    """Получить количество страниц.

    - start_date: дата начала поиска
    - end_date: дата конца поиска
    - name: наименование
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = CountTransactionSerializer(data=request.GET.dict())
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    params = {k: v[0] for k, v in dict(request.GET).items()}
    filter_data = {}
    for k, v in params.items():
        if k == 'user_id':
            filter_data['user_id'] = v
        if k == 'start_date':
            filter_data['date__gte'] = datetime.datetime.strptime(v, '%Y-%m-%d')
        if k == 'end_date':
            filter_data['date__lte'] = datetime.datetime.strptime(v, '%Y-%m-%d') + datetime.timedelta(days=1)
        if k == 'name':
            filter_data['name'] = v
    Transactions_count_page = math.ceil((Transaction.objects.filter(**filter_data).count() / 20))
    return Response({'count': Transactions_count_page}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', request_body=CreateTransactionSerializer, tags=['transaction'])
@api_view(['POST'])
@check_premission
def create(request):
    """Создать запись о транзакции.

    Входные параметры:
    ---
    - name: наименование расхода;
    - date: дата расхода;
    - amounnt: сумма расхода.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    create_Transaction = CreateTransactionSerializer(data=request.data)

    if not create_Transaction.is_valid():
        return Response(create_Transaction.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    
    name = create_Transaction.validated_data.get('name')
    date = create_Transaction.validated_data.get('date')
    amount = create_Transaction.validated_data.get('amount')
    user_id = create_Transaction.validated_data.get('user_id')
    fund_exists = Expense.objects.filter(name=name, user_id=user_id, amount__gte=amount)
    if not fund_exists:
        return Response({'ERORR': 'Нет фонда с таким именем или достаточной суммой'}, status=status.HTTP_404_NOT_FOUND)
    target_name = create_Transaction.validated_data.get('target_name')
    target_fund_exists = Expense.objects.filter(name=target_name, user_id=user_id)
    if not target_fund_exists:
        return Response({'ERORR': 'Нет фонда в счёт которого нужно проводить транзакцию'}, status=status.HTTP_404_NOT_FOUND)
    
    new_Transaction = Transaction.objects.create(name=name, date=date, amount=amount, user_id=user_id, target_name=target_name)
    data = model_to_dict(new_Transaction)
    return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='PATCH', request_body=UpdateTransactionSerializer, tags=['transaction'])
@api_view(['PATCH'])
@check_premission
def update(request):
    """Обновить запись о транзакции.

    Входные параметры:
    ---
    - name: наименование расхода;
    - date: дата расхода;
    - amounnt: сумма расхода.
    """
    if not request.method == 'PATCH':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        old_Transaction = Transaction.objects.get(pk=request.data.get('id'), user_id=request.data.get('user_id'))
    except Transaction.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    update_Transaction = UpdateTransactionSerializer(old_Transaction, data=request.data, partial=True)

    if not update_Transaction.is_valid():
        return Response(update_Transaction.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    update_Transaction.save()
    return Response(update_Transaction.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='PATCH', request_body=UpdateTransactionBulkSerializer, tags=['transaction'])
@api_view(['PATCH'])
@check_premission
def update_bulk(request):
    """Массово обновить запись о транзакции.

    Входные параметры:
    ---
    - items: список словарей;
    *тротлинг:50 записей; несуществующие расходы игнорируются.
    """
    if not request.method == 'PATCH':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = UpdateTransactionBulkSerializer(data=request.data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    objs = [Transaction(**obj) for obj in request.data['items']]
    fields = [k for k in request.data['items'][0].keys() if k != 'id']
    Transaction.objects.bulk_update(objs=objs, fields=fields, batch_size=25)
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='DELETE', query_serializer=DeleteTransactionSerializer, tags=['transaction'])
@api_view(['DELETE'])
@check_premission
def delete(request):
    """Удалить запись о транзакции.

    Входные параметры:
    ---
    -  id: идентификатор расхода.
    """
    if not request.method == 'DELETE':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_Transaction = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        Transaction = Transaction.objects.get(pk=id_Transaction, user_id=user_id)
    except Transaction.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    Transaction.delete()
    return Response({'status_delete': 'ok'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='DELETE', request_body=DeleteTransactionBulkSerializer, tags=['transaction'])
@api_view(['DELETE'])
@check_premission
def delete_bulk(request):
    """Массово удалить запись о транзакции.

    Входные параметры:
    ---
    - items: список id;
    *тротлинг:50 записей; несуществующие расходы игнорируются.
    """
    if not request.method == 'DELETE':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    reload_data = {
        'user_id': request.data['user_id'],
        'items': json.loads(request.data['items'])
    }
    serialaizer = DeleteTransactionBulkSerializer(data=reload_data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = reload_data['items']
    user_id = reload_data['user_id']

    transactions = Transaction.objects.filter(id__in=ids, user_id=user_id)
    if not transactions:
        return Response({'Error': 'transactions not found.'}, status=status.HTTP_404_NOT_FOUND)

    for transaction in transactions:
        transaction.delete()

    page=1
    limit = 20
    offset = (page * limit)-20 if (page > 1) else 0
    manager = Transaction.objects
    manager._using_default()
    transactions = Transaction.objects.filter(user_id=user_id).order_by('date')[offset:offset + limit]
    if not transactions:
        return Response({'items': []}, status=status.HTTP_200_OK)

    items = [model_to_dict(obj) for obj in transactions]
    return Response({'items': items}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', query_serializer=GetTransactionSerializer, tags=['transaction'])
@api_view(['GET'])
@check_premission
def get(request):
    """Получить запись о транзакции.

    Входные параметры:
    ---
    -  id: идентификатор расхода.
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_Transaction = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        Transaction = Transaction.objects.get(pk=id_Transaction, user_id=user_id)
    except Transaction.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    return Response(model_to_dict(Transaction), status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetTransactionBulkSerializer, tags=['transaction'])
@api_view(['GET'])
@check_premission
def get_bulk(request):
    """Массово получить запись о транзакции.

    Входные параметры:
    ---
    - page: номер страницы;
    - start_date: дата начала поиска
    - end_date: дата конца поиска
    - name: наименование
    *тротлинг:20 записей на страницу
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = GetTransactionBulkSerializer(data=request.GET.dict())
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    params = {k: v[0] for k, v in dict(request.GET).items()}
    page = int(params.pop('page'))
    user_id = int(params.get('user_id'))

    filter_data = {}
    for k, v in params.items():
        if k == 'user_id':
            filter_data['user_id'] = v
        if k == 'start_date':
            filter_data['date__gte'] = datetime.datetime.strptime(v, '%Y-%m-%d')
        if k == 'end_date':
            filter_data['date__lte'] = datetime.datetime.strptime(v, '%Y-%m-%d') + datetime.timedelta(days=1)
        if k == 'names':
            filter_data['name__in'] = json.loads(v)
    limit = 20
    offset = (page * limit)-20 if (page > 1) else 0
    transactions = Transaction.objects.filter(**filter_data).order_by('date')[offset:offset + limit]
    if not transactions:
        return Response({'Error': 'transactions not found.'}, status=status.HTTP_404_NOT_FOUND)

    items = [model_to_dict(obj) for obj in transactions]
    return Response({'items': items}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', query_serializer=CopyTransactionSerializer, tags=['transaction'])
@api_view(['POST'])
@check_premission
def copy(request):
    """Копировать запись о транзакции.

    Входные параметры:
    ---
    -  id: идентификатор расхода.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_Transaction = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        Transaction = Transaction.objects.get(pk=id_Transaction, user_id=user_id)
    except Transaction.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)
    params = model_to_dict(Transaction)
    params.pop('id')
    coping_Transaction = Transaction.objects.create(**params)

    return Response(model_to_dict(coping_Transaction), status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=CopyTransactionBulkSerializer, tags=['transaction'])
@api_view(['POST'])
@check_premission
def copy_bulk(request):
    """Массово копировать запись о транзакции.

    Входные параметры:
    ---
    - items: список id;
    *тротлинг:50 записей; несуществующие расходы игнорируются.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    reload_data = {
        'user_id': request.data['user_id'],
        'items': json.loads(request.data['items'])
    }
    serialaizer = CopyTransactionBulkSerializer(data=reload_data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = reload_data['items']
    user_id = reload_data['user_id']
    user = User.objects.get(pk=user_id)

    transactions = Transaction.objects.filter(id__in=ids, user_id=user_id)
    if not transactions:
        return Response({'Error': 'transactions not found.'}, status=status.HTTP_404_NOT_FOUND)
    obj_dicts = [model_to_dict(obj) for obj in transactions]
    [obj_dict.pop('id') for obj_dict in obj_dicts]
    obj_dicts_try = []
    for obj in obj_dicts:
        obj['user'] = user
        obj_dicts_try.append(obj)

    objs = [Transaction(**obj_dict) for obj_dict in obj_dicts]
    Transaction.objects.bulk_create(objs=objs, batch_size=25)
    page=1
    limit = 20
    offset = (page * limit)-20 if (page > 1) else 0
    manager = Transaction.objects
    manager._using_default()
    transactions = Transaction.objects.filter(user_id=user_id).order_by('date')[offset:offset + limit]
    items = [model_to_dict(obj) for obj in transactions]
    return Response({'items': items}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=DownloadFileSerializer, tags=['transaction'])
@api_view(['POST'])
@check_premission
def download_file(request):
    """Скачать файл"""
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    user_id = int(request.data['user_id'])
    start_date = request.data['start_date']
    end_date = request.data['end_date']
    separator = int(request.data['separator'])
    file_type = int(request.data['file_type'])

    data = Transaction.objects.filter(user_id=user_id, date__lte=end_date, date__gte=start_date)
    if not data:
        return Response({'Error': 'transactions not found.'}, status=status.HTTP_404_NOT_FOUND)
    headers = ['name', 'target_name', 'date', 'amount']
    data_list = data.values_list('name', 'target_name', 'date', 'amount')
    download_director = DownloadDirector(separator_type=separator, file_type=file_type, data=data_list, headers=headers)
    name_file = download_director.download()
    return Response({'path': f'{MEDIA_URL}temp_files/{name_file}'}, status=status.HTTP_201_CREATED)
