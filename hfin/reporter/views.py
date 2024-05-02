from .handlers import Reporter
import datetime
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from root.decorators import check_premission
from .serializers import (
    GetIncome,
    GetExpense,
    GetTransaction,
    GetIncomeGroup,
    GetExpenseGroup,
    GetYearsList,
    GetYearsDatasetTransaction,
    GetYearsDataset,
    GetYearsPredictExpense
)
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


@swagger_auto_schema(method='GET', query_serializer=GetIncomeGroup, tags=['Reporter'])
@api_view(['GET'])
@check_premission
def get_grouping_income(request):
    """Получить сгруппированные данные по доходам."""
    reporter = Reporter(
        user_id=request.GET.get('user_id'),
    )
    data = reporter.get_grouping_income()
    return Response(data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetExpenseGroup, tags=['Reporter'])
@api_view(['GET'])
@check_premission
def get_grouping_expense(request):
    """Получить сгруппированные данные по доходам."""
    reporter = Reporter(
        user_id=request.GET.get('user_id'),
    )
    data = reporter.get_grouping_expense()
    return Response(data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetYearsList, tags=['Reporter'])
@api_view(['GET'])
@check_premission
def get_years_list(request):
    """Получить список всех годов, которые есть в доходах или расходах."""
    reporter = Reporter(
        user_id=request.GET.get('user_id'),
    )
    data = reporter.get_years_list()

    return Response(list(data), status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetYearsDataset, tags=['Reporter'])
@api_view(['GET'])
@check_premission
def get_years_dataset(request):
    """Получит датасет по доходам и расходам."""

    reporter = Reporter(
        user_id=request.GET.get('user_id'),
    )
    data = reporter.get_years_dataset()

    return Response(list(data), status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetYearsDatasetTransaction, tags=['Reporter'])
@api_view(['GET'])
@check_premission
def get_years_dataset_transaction(request):
    """Получит датасет по транзакциям."""

    reporter = Reporter(
        user_id=request.GET.get('user_id'),
    )
    data = reporter.get_years_dataset_transaction()

    return Response(list(data), status=status.HTTP_200_OK)


@swagger_auto_schema(method='GET', query_serializer=GetYearsPredictExpense, tags=['Reporter'])
@api_view(['GET'])
@check_premission
def get_predict_day_of_year(request):
    """Получит датасет по транзакциям."""

    reporter = Reporter(
        user_id=request.GET.get('user_id'),
    )
    data = reporter.get_predict_day_of_year()

    return Response(list(data), status=status.HTTP_200_OK)
