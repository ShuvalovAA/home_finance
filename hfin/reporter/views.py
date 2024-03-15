from .handlers import Reporter
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from root.decorators import check_premission
from .serializers import GetIncome, GetExpense, GetTransaction
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from root.decorators import is_authenticated_and_is_active


@is_authenticated_and_is_active
def render_reporter_page(request):
    """Рендер на страницу отчётов."""
    return render(request, 'reporter.html')


@swagger_auto_schema(method='POST', request_body=GetIncome, tags=['Reporter'])
@api_view(['POST'])
@check_premission
def get_income(request):
    """Получить список доходов пользователя."""
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    request_data = GetIncome(data=request.data)
    if not request_data.is_valid():
        return Response(request_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    reporter = Reporter(
        user_id=request_data.data.get('user_id'),
        start_period=request_data.data.get('start_period'),
        end_period=request_data.data.get('end_period')
    )
    data = reporter.get_income()

    return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=GetIncome, tags=['Reporter'])
@api_view(['POST'])
@check_premission
def get_expense(request):
    """Получить список расходов пользователя."""
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    request_data = GetExpense(data=request.data)
    if not request_data.is_valid():
        return Response(request_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    reporter = Reporter(
        user_id=request_data.data.get('user_id'),
        start_period=request_data.data.get('start_period'),
        end_period=request_data.data.get('end_period')
    )
    data = reporter.get_expense()

    return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=GetIncome, tags=['Reporter'])
@api_view(['POST'])
@check_premission
def get_transaction(request):
    """Получить список транзакций пользователя."""
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    request_data = GetTransaction(data=request.data)
    if not request_data.is_valid():
        return Response(request_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    reporter = Reporter(
        user_id=request_data.data.get('user_id'),
        start_period=request_data.data.get('start_period'),
        end_period=request_data.data.get('end_period')
    )
    data = reporter.get_transaction()

    return Response(data, status=status.HTTP_201_CREATED)
