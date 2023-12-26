from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):
    """Форма авторизации."""

    phone = PhoneNumberField()
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    """Форма регистрации."""

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
