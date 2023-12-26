from django.forms.models import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transaction.models import Transaction

from .serializers import (
    CopyTransactionBulkSerializer,
    CopyTransactionSerializer,
    CreateTransactionSerializer,
    DeleteTransactionBulkSerializer,
    DeleteTransactionSerializer,
    GetTransactionBulkSerializer,
    GetTransactionSerializer,
    UpdateTransactionBulkSerializer,
    UpdateTransactionSerializer,
)


@swagger_auto_schema(method='POST', request_body=CreateTransactionSerializer, tags=['Transaction'])
@api_view(['POST'])
def create(request):
    """Создать запись о транзакции.

    Входные параметры:
    ---
    - name: наименование транзакции;
    - date: дата транзакции;
    - amounnt: сумма транзакции.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    create_transaction = CreateTransactionSerializer(data=request.data)

    if not create_transaction.is_valid():
        return Response(create_transaction.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    name = create_transaction.validated_data.get('name')
    date = create_transaction.validated_data.get('date')
    amount = create_transaction.validated_data.get('amount')
    done = create_transaction.validated_data.get('done')
    user_id = create_transaction.validated_data.get('user_id')
    new_transaction = Transaction.objects.create(name=name, date=date, amount=amount, done=done, user_id=user_id)
    data = model_to_dict(new_transaction)
    return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='PATCH', request_body=UpdateTransactionSerializer, tags=['Transaction'])
@api_view(['PATCH'])
def update(request):
    """Обновить запись о транзакции.

    Входные параметры:
    ---
    - name: наименование транзакции;
    - date: дата транзакции;
    - amounnt: сумма транзакции.
    """
    if not request.method == 'PATCH':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        old_transaction = Transaction.objects.get(pk=request.data.get('id'), user_id=request.data.get('user_id'))
    except Transaction.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    update_transaction = UpdateTransactionSerializer(old_transaction, data=request.data, partial=True)

    if not update_transaction.is_valid():
        return Response(update_transaction.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    update_transaction.save()
    return Response(update_transaction.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='PATCH', request_body=UpdateTransactionBulkSerializer, tags=['Transaction'])
@api_view(['PATCH'])
def update_bulk(request):
    """Массово обновить запись о транзакции.

    Входные параметры:
    ---
    - items: список словарей;
    *тротлинг:50 записей; несуществующие транзакции игнорируются.
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


@swagger_auto_schema(method='DELETE', query_serializer=DeleteTransactionSerializer, tags=['Transaction'])
@api_view(['DELETE'])
def delete(request):
    """Удалить запись о транзакции.

    Входные параметры:
    ---
    -  id: идентификатор транзакции.
    """
    if not request.method == 'DELETE':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_transaction = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        transaction = Transaction.objects.get(pk=id_transaction, user_id=user_id)
    except Transaction.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    transaction.delete()
    return Response({'status_delete': 'ok'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='DELETE', request_body=DeleteTransactionBulkSerializer, tags=['Transaction'])
@api_view(['DELETE'])
def delete_bulk(request):
    """Массово удалить запись о транзакции.

    Входные параметры:
    ---
    - items: список id;
    *тротлинг:50 записей; несуществующие транзакции игнорируются.
    """
    if not request.method == 'DELETE':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = DeleteTransactionBulkSerializer(data=request.data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = request.data['items']
    user_id = request.data['user_id']

    transactions = Transaction.objects.filter(pk__in=ids, user_id=user_id)
    if not transactions:
        return Response({'Error': 'Transactions not found.'}, status=status.HTTP_404_NOT_FOUND)
    transactions.delete()

    return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', query_serializer=GetTransactionSerializer, tags=['Transaction'])
@api_view(['GET'])
def get(request):
    """Получить запись о транзакции.

    Входные параметры:
    ---
    -  id: идентификатор транзакции.
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_transaction = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        transaction = Transaction.objects.get(pk=id_transaction, user_id=user_id)
    except Transaction.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    return Response(model_to_dict(transaction), status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetTransactionBulkSerializer, tags=['Transaction'])
@api_view(['GET'])
def get_bulk(request):
    """Массово получить запись о транзакции.

    Входные параметры:
    ---
    - page: номер страницы;
    *тротлинг:20 записей на страницу
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = GetTransactionBulkSerializer(data=request.GET.dict())
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    page = int(request.GET.get('page'))
    user_id = request.GET.get('user_id')
    limit = 20
    offset = page * limit if (page > 1) else 0
    transactions = Transaction.objects.filter(user_id=user_id)[offset:offset + limit]
    if not transactions:
        return Response({'Error': 'Transactions not found.'}, status=status.HTTP_404_NOT_FOUND)

    items = [model_to_dict(obj) for obj in transactions]
    return Response({'items': items}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', query_serializer=CopyTransactionSerializer, tags=['Transaction'])
@api_view(['POST'])
def copy(request):
    """Копировать запись о транзакции.

    Входные параметры:
    ---
    -  id: идентификатор транзакции.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_transaction = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        transaction = Transaction.objects.get(pk=id_transaction, user_id=user_id)
    except Transaction.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)
    params = model_to_dict(transaction)
    params.pop('id')
    coping_transaction = Transaction.objects.create(**params)

    return Response(model_to_dict(coping_transaction), status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=CopyTransactionBulkSerializer, tags=['Transaction'])
@api_view(['POST'])
def copy_bulk(request):
    """Массово копировать запись о транзакции.

    Входные параметры:
    ---
    - items: список id;
    *тротлинг:50 записей; несуществующие транзакции игнорируются.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = CopyTransactionBulkSerializer(data=request.data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = request.data['items']
    user_id = request.data['user_id']

    transactions = Transaction.objects.filter(pk__in=ids, user_id=user_id)
    if not transactions:
        return Response({'Error': 'Transactions not found.'}, status=status.HTTP_404_NOT_FOUND)
    obj_dicts = [model_to_dict(obj) for obj in transactions]
    [obj_dict.pop('id') for obj_dict in obj_dicts]

    objs = [Transaction(**obj_dict) for obj_dict in obj_dicts]
    Transaction.objects.bulk_create(objs=objs, batch_size=25)
    return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
