from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User


class GetUserSerializer(serializers.Serializer):
    """Сериалайзер для получения информации по пользователю."""

    id = serializers.IntegerField()


class UpdateUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для обновления пользовательских данных."""

    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=124)
    last_name = serializers.CharField(max_length=124)
    middle_name = serializers.CharField(max_length=124)
    email = serializers.EmailField(max_length=254)
    birth_date = serializers.DateTimeField()
    register_date = serializers.DateField()
    sms_subcribe = serializers.BooleanField()
    email_subcribe = serializers.BooleanField()
    is_active = serializers.BooleanField()
    phone = PhoneNumberField()
    is_phone_confirm = serializers.BooleanField()
    is_email_confirm = serializers.BooleanField()

    class Meta:
        """Метаданные сериалайзера."""

        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'birth_date',
            'register_date',
            'sms_subcribe',
            'email_subcribe',
            'is_active',
            'phone',
            'is_phone_confirm',
            'is_email_confirm'
        ]


class UpdateUserLightSerializer(serializers.Serializer):
    """Сериалайзер для обновления пользовательских данных лёгкий."""

    user_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=124)
    last_name = serializers.CharField(max_length=124)
    middle_name = serializers.CharField(max_length=124)
    birth_date = serializers.DateTimeField()
