import requests
from root import settings


class SmsHandler():
    """Обработчик отправки sms."""

    def __init__(self):
        self.login = settings.SMS_CONFIG['login']
        self.secret_key = settings.SMS_CONFIG['secret_key']
        self.password = settings.SMS_CONFIG['password']
        self.url = settings.SMS_CONFIG['url']

    def send_sms(self, user, text):
        """Отправить sms"""
        params = {
            'phone': user.phone.__str__(),
            'text': text
        }
        requests.post(
            url=self.url,
            login=self.login,
            password=self.password,
            data=params
        )


sms_handler = SmsHandler()
