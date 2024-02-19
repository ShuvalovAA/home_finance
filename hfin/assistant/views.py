from drf_yasg.utils import swagger_auto_schema
from expense.models import Expense
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from root.decorators import check_premission
from user.models import User

from .serializers import GetPredictSerializer
from .handlers import ml_linear_regression


@swagger_auto_schema(method='get', query_serializer=GetPredictSerializer, tags=['Predict'])
@api_view(['GET'])
@check_premission
def predict_day_of_year(request):
    """Получить предсказание расхода на день года."""
    if not request.method == 'GET':
        return Response({'Error': 'Invalid request type'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    expense_predict = GetPredictSerializer(data=request.GET)

    if not expense_predict.is_valid():
        return Response(expense_predict.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    user_id = expense_predict.validated_data.get('user_id')
    expense_name = expense_predict.validated_data.get('expense_name')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)

    try:
        result, mode, median = ml_linear_regression.get_prediction(
            user, expense_name.lower()
        )
    except Expense.DoesNotExist as error:
        return Response(error.__str__(), status=status.HTTP_404_NOT_FOUND)
    data = {
        "user_id": user_id,
        "expense_name": expense_name,
        "mode": mode,
        "median": median,
        "predict_amounts_by_month_of_year": result
    }
    return Response(data, status=status.HTTP_201_CREATED)
