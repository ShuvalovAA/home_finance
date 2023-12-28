from django.forms.models import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from expense.models import Expense
from rest_framework import parsers, renderers, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from root.decorators import check_premission

from .serializers import (
    CopyExpenseBulkSerializer,
    CopyExpenseSerializer,
    CreateBulkExpenseSerializer,
    CreateExpenseSerializer,
    DeleteExpenseBulkSerializer,
    DeleteExpenseSerializer,
    GetExpenseBulkSerializer,
    GetExpenseSerializer,
    UpdateExpenseBulkSerializer,
    UpdateExpenseSerializer,
)


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

    create_expense = CreateExpenseSerializer(data=request.data)

    if not create_expense.is_valid():
        return Response(create_expense.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    name = create_expense.validated_data.get('name')
    date = create_expense.validated_data.get('date')
    amount = create_expense.validated_data.get('amount')
    done = create_expense.validated_data.get('done')
    user_id = create_expense.validated_data.get('user_id')
    new_expense = Expense.objects.create(name=name, date=date, amount=amount, done=done, user_id=user_id)
    data = model_to_dict(new_expense)
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
        old_expense = Expense.objects.get(pk=request.data.get('id'), user_id=request.data.get('user_id'))
    except Expense.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    update_expense = UpdateExpenseSerializer(old_expense, data=request.data, partial=True)

    if not update_expense.is_valid():
        return Response(update_expense.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    update_expense.save()
    return Response(update_expense.data, status=status.HTTP_200_OK)


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

    id_expense = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        expense = Expense.objects.get(pk=id_expense, user_id=user_id)
    except Expense.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    expense.delete()
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

    serialaizer = DeleteExpenseBulkSerializer(data=request.data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = request.data['items']
    user_id = request.data['user_id']

    expenses = Expense.objects.filter(pk__in=ids, user_id=user_id)
    if not expenses:
        return Response({'Error': 'Expenses not found.'}, status=status.HTTP_404_NOT_FOUND)
    expenses.delete()

    return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)


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

    id_expense = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        expense = Expense.objects.get(pk=id_expense, user_id=user_id)
    except Expense.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    return Response(model_to_dict(expense), status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetExpenseBulkSerializer, tags=['Expense'])
@api_view(['GET'])
@check_premission
def get_bulk(request):
    """Массово получить запись о расходе.

    Входные параметры:
    ---
    - page: номер страницы;
    *тротлинг:20 записей на страницу
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = GetExpenseBulkSerializer(data=request.GET.dict())
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    user_id = request.GET.get('user_id')
    page = int(request.GET.get('page'))
    limit = 20
    offset = page * limit if (page > 1) else 0
    expenses = Expense.objects.filter(user_id=user_id)[offset:offset + limit]
    if not expenses:
        return Response({'Error': 'Expenses not found.'}, status=status.HTTP_404_NOT_FOUND)

    items = [model_to_dict(obj) for obj in expenses]
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

    id_expense = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        expense = Expense.objects.get(pk=id_expense, user_id=user_id)
    except Expense.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)
    params = model_to_dict(expense)
    params.pop('id')
    coping_expense = Expense.objects.create(**params)

    return Response(model_to_dict(coping_expense), status=status.HTTP_201_CREATED)


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

    serialaizer = CopyExpenseBulkSerializer(data=request.data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = request.data['items']
    user_id = request.data['user_id']

    expenses = Expense.objects.filter(pk__in=ids, user_id=user_id)
    if not expenses:
        return Response({'Error': 'Expenses not found.'}, status=status.HTTP_404_NOT_FOUND)
    obj_dicts = [model_to_dict(obj) for obj in expenses]
    [obj_dict.pop('id') for obj_dict in obj_dicts]

    objs = [Expense(**obj_dict) for obj_dict in obj_dicts]
    Expense.objects.bulk_create(objs=objs, batch_size=25)
    return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)


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
