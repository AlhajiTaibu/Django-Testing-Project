from django.urls import reverse
from pytest_factoryboy import register
import pytest
from factories import UserFactory, BlogFactory
from Auth.models import User
from rest_framework.test import APIClient

register(UserFactory)
register(BlogFactory)


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        kwargs['password'] = "pAssw0rd1"
        user = User.objects.create_user(email=kwargs['email'], password=kwargs['password'])
        if 'is_staff' in kwargs:
            user.is_staff = kwargs['is_staff']
        user.is_activated = True
        user.is_active = True
        user.save()
        return user

    return make_user


@pytest.fixture(scope="module")
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client, db):
    def authenticate_user(**kwargs):
        user = kwargs['user']
        token_url = reverse('GetTokenPair')
        data = {'email': user.email, 'password': 'pAssw0rd1'}
        token_response = api_client.post(path=token_url, data=data)
        token_pair = token_response.data
        api_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token_pair["access"]}'
        )
        return

    return authenticate_user

