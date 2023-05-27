from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        validators=(UniqueValidator(queryset=User.objects.all()),),
        max_length=150
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserSignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        validators=(UniqueValidator(queryset=User.objects.all()),),
        max_length=150
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        max_length=254
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate(self, attr):
        if attr['username'] == 'me':
            raise serializers.ValidationError(
                'Регистрация с именем "me" запрещена'
            )

        return attr

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токенов."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'confirmation_code',
            'username'
        )
