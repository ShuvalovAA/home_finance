from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view


@swagger_auto_schema(method='PATCH', tags=['User'])
@api_view(['PATCH'])
def update(request):
    """Обновить данные пользователя."""
    pass


@swagger_auto_schema(method='GET', tags=['User'])
@api_view(['GET'])
def get(request):
    """Получить данные пользователя."""
    pass
