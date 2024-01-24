from .serializers import FundsBuilderExpense, FundsBuilderIncome, FundsBuilderTransaction
from .handlers import FundsDirector
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from root.decorators import check_premission
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='POST', request_body=FundsBuilderIncome, tags=['FundsBuild'])
@api_view(['POST'])
@check_premission
def build_funds_income(request):
    """Получить фондов доходов пользователя."""
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    request_data = FundsBuilderIncome(data=request.data)
    if not request_data.is_valid():
        return Response(request_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    reporter = FundsDirector(user_id=request_data.data.get('user_id'))
    data = reporter.build_funds_income()

    return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=FundsBuilderExpense, tags=['FundsBuild'])
@api_view(['POST'])
@check_premission
def build_funds_expense(request):
    """Получить фондов расходов пользователя."""
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    request_data = FundsBuilderExpense(data=request.data)
    if not request_data.is_valid():
        return Response(request_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    reporter = FundsDirector(user_id=request_data.data.get('user_id'))
    data = reporter.build_funds_expense()

    return Response(data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='POST', request_body=FundsBuilderTransaction, tags=['FundsBuild'])
@api_view(['POST'])
@check_premission
def build_funds_transaction(request):
    """Получить фондов транзакций пользователя."""
    if not request.method == 'POST':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    request_data = FundsBuilderTransaction(data=request.data)
    if not request_data.is_valid():
        return Response(request_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    reporter = FundsDirector(user_id=request_data.data.get('user_id'))
    data = reporter.build_funds_transaction()

    return Response(data, status=status.HTTP_201_CREATED)
