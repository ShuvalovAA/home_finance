import requests
from root import settings


class EmailHandler():
    """Обработчик отправки email."""

    def __init__(self):
        self.login = settings.EMAIL_CONFIG['login']
        self.secret_key = settings.EMAIL_CONFIG['secret_key']
        self.password = settings.EMAIL_CONFIG['password']
        self.url = settings.EMAIL_CONFIG['url']

    def send_email(self, user, text):
        """Отправить email"""
        params = {
            'phone': user.email,
            'text': text
        }
        requests.post(
            url=self.url,
            login=self.login,
            password=self.password,
            data=params
        )


email_handler = EmailHandler()
