from rest_framework import generics
from .serializers import RegistrationSerializer, UserAuthenticationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer


class Authentication(TokenObtainPairView):
    serializer_class = UserAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
