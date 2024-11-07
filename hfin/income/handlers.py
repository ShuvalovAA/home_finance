from income.models import Income
from django.http import HttpRequest


def get_object(request: HttpRequest) -> Income:
    """Метод получения объекта"""
    id_income = request.GET.get('id')
    user_id = request.GET.get('user_id')
    return Income.objects.get(pk=id_income, user_id=user_id)
