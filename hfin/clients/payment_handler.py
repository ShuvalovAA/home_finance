import requests
from root import settings
from payment.models import UsersPayments
from datetime import datetime

class PaymentHandler():
    """Обработчик платежей."""

    def __init__(self):
        self.login = settings.EMAIL_CONFIG['login']
        self.secret_key = settings.EMAIL_CONFIG['secret_key']
        self.password = settings.EMAIL_CONFIG['password']
        self.url = settings.EMAIL_CONFIG['url']

    def send_payment(self, user, product, amount):
        """Отправить платёж"""
        params = {
            'user_id': user.id,
            'product': product,
            'amount': amount,
            'login': self.login,
            'password': self.password,
        }
        response = requests.post(
            url=self.url,
            data=params
        )
        #return response.get('target_url')
        params = {
            'user': user,
            'date': datetime.now(),
            'tariff': product,
            'done': False
        }
        payment = UsersPayments.objects.create(**params)
        return 'http://www.yandex.ru'

    def webhook_get_pay(self, params):
        """Получить платёж."""
        user = params.get('user')
        tariff = params.get('tariff')
        breakpoint()
        payment = UsersPayments.objects.get(
            user=user,
            tariff=tariff,
            done=False
        )
        payment.update(**params)
        user.activate_subscription()


payment_handler = PaymentHandler()
