from celery_app import CELERY_APP
from income.models import Income
from expense.models import Expense
from payment.models import UsersPayments



@CELERY_APP.task(name='check_getting_income')
def check_getting_income():
    data = Income.objects.all()
    print(data)


@CELERY_APP.task(name='check_expired_subscribies')
def check_expired_subscribies():
    """Таска проверки подписки пользователей.

    Таска ищет пользователей, у которых фактически срок подписки истёк, но не изменён флаг.
    """
    #todo
    data = UsersPayments.objects.all()
    print(data)


@CELERY_APP.task(name='check_expiring_subscribies')
def check_expiring_subscribies():
    """Таска проверки подписки пользователей.

    Таска ищет пользователей, у которых срок подписки скоро истечёт, для оповещения.
    """
    #todo
    data = UsersPayments.objects.all()
    print(data)
