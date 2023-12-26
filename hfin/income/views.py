from django.forms.models import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from income.models import Income
from rest_framework import parsers, renderers, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from root.decorators import check_premission

from .serializers import (
    CopyIncomeBulkSerializer,
    CopyIncomeSerializer,
    CreateBulkIncomeSerializer,
    CreateIncomeSerializer,
    DeleteIncomeBulkSerializer,
    DeleteIncomeSerializer,
    GetIncomeBulkSerializer,
    GetIncomeSerializer,
    UpdateIncomeBulkSerializer,
    UpdateIncomeSerializer,
)


@swagger_auto_schema(method='POST', request_body=CreateIncomeSerializer, tags=['Income'])
@api_view(['POST'])
def create(request):
    """Создать запись о доходе.

    Входные параметры:
    ---
    - name: наименование дохода;
    - date: дата дохода;
    - amounnt: сумма дохода.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    create_income = CreateIncomeSerializer(data=request.data)

    if not create_income.is_valid():
        return Response(create_income.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    name = create_income.validated_data.get('name')
    date = create_income.validated_data.get('date')
    amount = create_income.validated_data.get('amount')
    done = create_income.validated_data.get('done')
    user_id = create_income.validated_data.get('user_id')
    new_income = Income.objects.create(name=name, date=date, amount=amount, done=done, user_id=user_id)
    data = model_to_dict(new_income)
    return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='PATCH', request_body=UpdateIncomeSerializer, tags=['Income'])
@api_view(['PATCH'])
def update(request):
    """Обновить запись о доходе.

    Входные параметры:
    ---
    - name: наименование дохода;
    - date: дата дохода;
    - amounnt: сумма дохода.
    """
    if not request.method == 'PATCH':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        old_income = Income.objects.get(pk=request.data.get('id'), user_id=request.data.get('user_id'))
    except Income.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    update_income = UpdateIncomeSerializer(old_income, data=request.data, partial=True)

    if not update_income.is_valid():
        return Response(update_income.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    update_income.save()
    return Response(update_income.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='PATCH', request_body=UpdateIncomeBulkSerializer, tags=['Income'])
@api_view(['PATCH'])
def update_bulk(request):
    """Массово обновить запись о доходе.

    Входные параметры:
    ---
    - items: список словарей;
    *тротлинг:50 записей; несуществующие доходы игнорируются.
    """
    if not request.method == 'PATCH':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = UpdateIncomeBulkSerializer(data=request.data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    objs = [Income(**obj) for obj in request.data['items']]
    fields = [k for k in request.data['items'][0].keys() if k != 'id']
    Income.objects.bulk_update(objs=objs, fields=fields, batch_size=25)
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='DELETE', query_serializer=DeleteIncomeSerializer, tags=['Income'])
@api_view(['DELETE'])
def delete(request):
    """Удалить запись о доходе.

    Входные параметры:
    ---
    -  id: идентификатор дохода.
    """
    if not request.method == 'DELETE':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_income = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        income = Income.objects.get(pk=id_income, user_id=user_id)
    except Income.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    income.delete()
    return Response({'status_delete': 'ok'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='DELETE', request_body=DeleteIncomeBulkSerializer, tags=['Income'])
@api_view(['DELETE'])
def delete_bulk(request):
    """Массово удалить запись о доходе.

    Входные параметры:
    ---
    - items: список id;
    *тротлинг:50 записей; несуществующие доходы игнорируются.
    """
    if not request.method == 'DELETE':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = DeleteIncomeBulkSerializer(data=request.data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = request.data['items']
    user_id = request.data['user_id']

    incomes = Income.objects.filter(pk__in=ids, user_id=user_id)
    if not incomes:
        return Response({'Error': 'Incomes not found.'}, status=status.HTTP_404_NOT_FOUND)
    incomes.delete()

    return Response({'status': 'ok'}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', query_serializer=GetIncomeSerializer, tags=['Income'])
@api_view(['GET'])
def get(request):
    """Получить запись о доходе.

    Входные параметры:
    ---
    -  id: идентификатор дохода.
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_income = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        income = Income.objects.get(pk=id_income, user_id=user_id)
    except Income.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    return Response(model_to_dict(income), status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetIncomeBulkSerializer, tags=['Income'])
@api_view(['GET'])
@check_premission
def get_bulk(request):
    """Массово получить запись о доходе.

    Входные параметры:
    ---
    - page: номер страницы;
    *тротлинг:20 записей на страницу
    """
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = GetIncomeBulkSerializer(data=request.GET.dict())
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    page = int(request.GET.get('page'))
    user_id = request.GET.get('user_id')
    limit = 20
    offset = page * limit if (page > 1) else 0
    incomes = Income.objects.filter(user_id=user_id)[offset:offset + limit]
    if not incomes:
        return Response({'Error': 'Incomes not found.'}, status=status.HTTP_404_NOT_FOUND)

    items = [model_to_dict(obj) for obj in incomes]
    return Response({'items': items}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', query_serializer=CopyIncomeSerializer, tags=['Income'])
@api_view(['POST'])
def copy(request):
    """Копировать запись о доходе.

    Входные параметры:
    ---
    -  id: идентификатор дохода.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    id_income = request.GET.get('id')
    user_id = request.GET.get('user_id')
    try:
        income = Income.objects.get(pk=id_income, user_id=user_id)
    except Income.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)
    params = model_to_dict(income)
    params.pop('id')
    coping_income = Income.objects.create(**params)

    return Response(model_to_dict(coping_income), status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=CopyIncomeBulkSerializer, tags=['Income'])
@api_view(['POST'])
def copy_bulk(request):
    """Массово копировать запись о доходе.

    Входные параметры:
    ---
    - items: список id;
    *тротлинг:50 записей; несуществующие доходы игнорируются.
    """
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    serialaizer = CopyIncomeBulkSerializer(data=request.data)
    if not serialaizer.is_valid():
        return Response(serialaizer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ids = request.data['items']
    user_id = request.data['user_id']

    incomes = Income.objects.filter(pk__in=ids, user_id=user_id)
    if not incomes:
        return Response({'Error': 'Incomes not found.'}, status=status.HTTP_404_NOT_FOUND)
    obj_dicts = [model_to_dict(obj) for obj in incomes]
    [obj_dict.pop('id') for obj_dict in obj_dicts]

    objs = [Income(**obj_dict) for obj_dict in obj_dicts]
    Income.objects.bulk_create(objs=objs, batch_size=25)
    return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)


class CreateBulkIncomeView(GenericAPIView):
    """Класс вью массовой загрузки доходов посредством файла."""

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CreateBulkIncomeSerializer
    tags = ['Income']

    @swagger_auto_schema(tags=['Income'])
    def post(self, request):
        """Массовое добавление записей о доходах файлом.

        Входные параметры:
        ---
        -  file: файл, который содержит записи о доходах.*без указания заголовков
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
