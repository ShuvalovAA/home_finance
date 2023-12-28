from django.core.exceptions import PermissionDenied
from user.models import User


def check_premission(method, *args, **kwargs):
    """Декоратор проверки доступа к функционалу API.

    API доступен только если:
    - 1: пользователь делает запрос сам по себе;
    - 2: запрос по пользователю делает сервисный аккаунт.
    """

    def wrapper(*args, **kwargs):
        request = args[0]
        request_user_id = request.user.id

        if not request_user_id:
            raise PermissionDenied

        params_get_user_id = request.GET.get('user_id')
        params_data_user_id = request.data.get('user_id')
        params_user_id = params_get_user_id or params_data_user_id

        if not params_user_id:
            raise PermissionDenied

        try:
            user = User.objects.get(pk=request_user_id)
        except User.DoesNotExist:
            raise PermissionDenied

        is_permission = any([
            user.is_service_account,
            request_user_id == int(params_user_id)
        ])

        if not is_permission:
            raise PermissionDenied
        res = method(*args, **kwargs)
        return res
    return wrapper
