from rest_framework import serializers
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if len(attrs["password"]) < 8:
            raise serializers.ValidationError({
                "error": "passwords should be more than 8 characters"
            })
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)


class UserAuthenticationSerializer(TokenObtainPairSerializer):

    class Meta:
        model = User
        fields = ['email',
                  'is_staff', 'is_active', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(
            read_only=True
        )
        self.fields['email'] = serializers.CharField()

    def validate(self, attrs):
        attrs[self.username_field] = attrs['email']
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        data = super().validate(attrs)
        return data
