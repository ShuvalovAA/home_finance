import json
import datetime
import math
from django.forms.models import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from expense.models import Expense
from rest_framework import parsers, renderers, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from root.decorators import check_premission, is_authenticated_and_is_active
from django.shortcuts import render
from user.models import User


from .serializers import (
    NamesExpenseSerializer,
    CopyExpenseBulkSerializer,
    CopyExpenseSerializer,
    CreateBulkExpenseSerializer,
    CreateExpenseSerializer,
    DeleteExpenseBulkSerializer,
    DeleteExpenseSerializer,
    CountExpenseSerializer,
    GetExpenseBulkSerializer,
    GetExpenseSerializer,
    UpdateExpenseBulkSerializer,
    UpdateExpenseSerializer,
)


@is_authenticated_and_is_active
def render_Expense_page(request):
    """Рендер на страницу расходов."""
    return render(request, 'Expense.html')


@swagger_auto_schema(method='GET', query_serializer=NamesExpenseSerializer, tags=['Expense'])
@api_view(['GET'])
@check_premission
def get_name_list(request):
    user_id = request.GET.get('user_id')
    manager = Expense.objects
    manager._using_default()
    names = list(Expense.objects.filter(user_id=user_id).distinct("name").values_list('name', flat=True))
    return Response({'names': names}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=CountExpenseSerializer, tags=['Expense'])
@api_view(['GET'])
@check_premission
def get_count_for_paggination(request):
    """Получить количество страниц.

    - start_date: дата начала поиска
    - end_date: дата конца поиска
    - name: наименование
    - done: статус выполнения
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = CountExpenseSerializer(data=request.GET.dict())
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    params = {k: v[0] for k, v in dict(request.GET).items()}
    user_id = int(params.get('user_id'))

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
        if k == 'done':
            if v == 'true':
                filter_data['done'] = True
            if v == 'false':
                filter_data['done'] = False
    Expenses_count_page = math.ceil((Expense.objects.filter(**filter_data).count() / 20))
    return Response({'count': Expenses_count_page}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', request_body=CreateExpenseSerializer, tags=['Expense'])
@api_view(['POST'])
@check_premission
def create(request):
    """Создать запись о расходе.

    Входные параметры:
    ---
    - name: наименование расхода;
    - date: дата расхода;
    - amounnt: сумма расхода.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    create_Expense = CreateExpenseSerializer(data=request.data)

    if not create_Expense.is_valid():
        return Response(create_Expense.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    name = create_Expense.validated_data.get('name')
    date = create_Expense.validated_data.get('date')
    amount = create_Expense.validated_data.get('amount')
    done = create_Expense.validated_data.get('done')
    user_id = create_Expense.validated_data.get('user_id')
    new_Expense = Expense.objects.create(name=name, date=date, amount=amount, done=done, user_id=user_id)
    data = model_to_dict(new_Expense)
    return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='PATCH', request_body=UpdateExpenseSerializer, tags=['Expense'])
@api_view(['PATCH'])
@check_premission
def update(request):
    """Обновить запись о расходе.

    Входные параметры:
    ---
    - name: наименование расхода;
    - date: дата расхода;
    - amounnt: сумма расхода.
    """
    if not request.method == 'PATCH':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        old_Expense = Expense.objects.get(pk=request.data.get('id'), user_id=request.data.get('user_id'))
    except Expense.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    update_Expense = UpdateExpenseSerializer(old_Expense, data=request.data, partial=True)

    if not update_Expense.is_valid():
        return Response(update_Expense.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    update_Expense.save()
    return Response(update_Expense.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='PATCH', request_body=UpdateExpenseBulkSerializer, tags=['Expense'])
@api_view(['PATCH'])
@check_premission
def update_bulk(request):
    """Массово обновить запись о расходе.

    Входные параметры:
    ---
    - items: список словарей;
    *тротлинг:50 записей; несуществующие расходы игнорируются.
    """
    if not request.method == 'PATCH':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = UpdateExpenseBulkSerializer(data=request.data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    objs = [Expense(**obj) for obj in request.data['items']]
    fields = [k for k in request.data['items'][0].keys() if k != 'id']
    Expense.objects.bulk_update(objs=objs, fields=fields, batch_size=25)
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='DELETE', query_serializer=DeleteExpenseSerializer, tags=['Expense'])
@api_view(['DELETE'])
@check_premission
def delete(request):
    """Удалить запись о расходе.

    Входные параметры:
    ---
    -  id: идентификатор расхода.
    """
    if not request.method == 'DELETE':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_Expense = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        Expense = Expense.objects.get(pk=id_Expense, user_id=user_id)
    except Expense.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    Expense.delete()
    return Response({'status_delete': 'ok'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='DELETE', request_body=DeleteExpenseBulkSerializer, tags=['Expense'])
@api_view(['DELETE'])
@check_premission
def delete_bulk(request):
    """Массово удалить запись о расходе.

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
    serialaizer = DeleteExpenseBulkSerializer(data=reload_data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = reload_data['items']
    user_id = reload_data['user_id']

    Expenses = Expense.objects.filter(id__in=ids, user_id=user_id)
    if not Expenses:
        return Response({'Error': 'Expenses not found.'}, status=status.HTTP_404_NOT_FOUND)

    for Expense in Expenses:
        Expense.delete()

    page=1
    limit = 20
    offset = (page * limit)-20 if (page > 1) else 0
    manager = Expense.objects
    manager._using_default()
    Expenses = Expense.objects.filter(user_id=user_id).order_by('date')[offset:offset + limit]
    if not Expenses:
        return Response({'items': []}, status=status.HTTP_200_OK)

    items = [model_to_dict(obj) for obj in Expenses]
    return Response({'items': items}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', query_serializer=GetExpenseSerializer, tags=['Expense'])
@api_view(['GET'])
@check_premission
def get(request):
    """Получить запись о расходе.

    Входные параметры:
    ---
    -  id: идентификатор расхода.
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_Expense = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        Expense = Expense.objects.get(pk=id_Expense, user_id=user_id)
    except Expense.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    return Response(model_to_dict(Expense), status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetExpenseBulkSerializer, tags=['Expense'])
@api_view(['GET'])
@check_premission
def get_bulk(request):
    """Массово получить запись о расходе.

    Входные параметры:
    ---
    - page: номер страницы;
    - start_date: дата начала поиска
    - end_date: дата конца поиска
    - name: наименование
    - done: статус выполнения
    *тротлинг:20 записей на страницу
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = GetExpenseBulkSerializer(data=request.GET.dict())
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
        if k == 'name':
            filter_data['name'] = v
        if k == 'done':
            if v == 'true':
                filter_data['done'] = True
            if v == 'false':
                filter_data['done'] = False
    limit = 20
    offset = (page * limit)-20 if (page > 1) else 0
    Expenses = Expense.objects.filter(**filter_data).order_by('date')[offset:offset + limit]
    if not Expenses:
        return Response({'Error': 'Expenses not found.'}, status=status.HTTP_404_NOT_FOUND)

    items = [model_to_dict(obj) for obj in Expenses]
    return Response({'items': items}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', query_serializer=CopyExpenseSerializer, tags=['Expense'])
@api_view(['POST'])
@check_premission
def copy(request):
    """Копировать запись о расходе.

    Входные параметры:
    ---
    -  id: идентификатор расхода.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_Expense = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        Expense = Expense.objects.get(pk=id_Expense, user_id=user_id)
    except Expense.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)
    params = model_to_dict(Expense)
    params.pop('id')
    coping_Expense = Expense.objects.create(**params)

    return Response(model_to_dict(coping_Expense), status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=CopyExpenseBulkSerializer, tags=['Expense'])
@api_view(['POST'])
@check_premission
def copy_bulk(request):
    """Массово копировать запись о расходе.

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
    serialaizer = CopyExpenseBulkSerializer(data=reload_data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = reload_data['items']
    user_id = reload_data['user_id']
    user = User.objects.get(pk=user_id)

    Expenses = Expense.objects.filter(id__in=ids, user_id=user_id)
    if not Expenses:
        return Response({'Error': 'Expenses not found.'}, status=status.HTTP_404_NOT_FOUND)
    obj_dicts = [model_to_dict(obj) for obj in Expenses]
    [obj_dict.pop('id') for obj_dict in obj_dicts]
    obj_dicts_try = []
    for obj in obj_dicts:
        obj['user'] = user
        obj_dicts_try.append(obj)

    objs = [Expense(**obj_dict) for obj_dict in obj_dicts]
    Expense.objects.bulk_create(objs=objs, batch_size=25)
    page=1
    limit = 20
    offset = (page * limit)-20 if (page > 1) else 0
    manager = Expense.objects
    manager._using_default()
    Expenses = Expense.objects.filter(user_id=user_id).order_by('date')[offset:offset + limit]
    items = [model_to_dict(obj) for obj in Expenses]
    return Response({'items': items}, status=status.HTTP_201_CREATED)


class CreateBulkExpenseView(GenericAPIView):
    """Класс вью массовой загрузки расходов посредством файла."""

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CreateBulkExpenseSerializer
    tags = ['Expense']

    @swagger_auto_schema(tags=['Expense'])
    @check_premission
    def post(self, request):
        """Массовое добавление записей о расходах файлом.

        Входные параметры:
        ---
        -  file: файл, который содержит записи о расходах.*без указания заголовков
        ---
        *Требования*:

            маппинг: [ namer: str | date: str(datetime) | amount: str(decimal)]
            кодировка: utf-8
            формат: csv
            разделитель: ';'
        ---
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # data = serializer.validated_data
            # file = data['file']
            breakpoint()
            return Response({'status': 'ok'})
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
