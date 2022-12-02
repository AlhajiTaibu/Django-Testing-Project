from django.urls import path

from .views import RegistrationView, Authentication

urlpatterns = [
    path(
        'register',
        RegistrationView.as_view(),
        name="register"
    ),
    path(
        'token',
        Authentication.as_view(),
        name="GetTokenPair"
    ),
]
