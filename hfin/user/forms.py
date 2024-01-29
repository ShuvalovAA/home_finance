from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from captcha.fields import CaptchaField

from .models import User


class LoginForm(forms.Form):
    """Форма авторизации."""

    phone = PhoneNumberField()
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    captcha = CaptchaField()


class ConfirmSMS(forms.Form):
    """Форма подтверждения по sms."""

    code = forms.CharField(max_length=6)
    user_id = forms.IntegerField()
    register = forms.IntegerField()


class RegisterForm(UserCreationForm):
    """Форма регистрации."""

    captcha = CaptchaField()

    class Meta:
        """Метаданный формы регистрации."""

        model = User
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'birth_date',
            'sms_subcribe',
            'email_subcribe',
            'phone'
        ]
