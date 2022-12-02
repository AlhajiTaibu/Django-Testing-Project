from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from Blog.models import BlogPost


class TestBlogPost(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_staffuser(
            email="staff@gmail.com", password="pAssw0rd1"
        )
        cls.user.is_activated = True
        cls.user.is_active = True
        cls.user.is_staff = True
        cls.user.save()

        cls.bus_user = get_user_model().objects.create_user(
            email="business@gmail.com", password="pAssw0rd1"
        )
        cls.bus_user.is_activated = True
        cls.bus_user.is_staff = True
        cls.bus_user.save()

        cls.user_3 = get_user_model().objects.create_user(
            username="Normal",
            email="user@gmail.com", password="pAssw0rd1"
        )
        cls.user_3.is_activated = True
        cls.user_3.is_active = True
        cls.user_3.save()

        cls.data = {
            'owner': cls.user,
            'title': 'Third Post',
            'description': 'This is the third post',
            'email': cls.user.email,
            'phone_number': '0245896732'
        }
        cls.data_1 = {
            'owner': cls.bus_user,
            'title': 'Third Post',
            'description': 'This is the third post',
            'email': cls.bus_user.email,
            'phone_number': '0245896732'
        }
        cls.blog = BlogPost.objects.create(**cls.data)
        cls.blog_1 = BlogPost.objects.create(**cls.data_1)

    def authenticate_user(self, email):
        token_url = reverse('GetTokenPair')
        data = {'email': email, 'password': 'pAssw0rd1'}
        token_response = self.client.post(path=token_url, data=data)
        token_pair = token_response.data
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token_pair["access"]}'
        )

    def test_blog_post_creation_by_staff(self):
        self.authenticate_user(self.user.email)
        path = reverse('create-post')

        data = {
            'owner': self.user,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': self.user.email,
            'phone_number': '0245896732'
        }
        create_response = self.client.post(path=path, data=data)
        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(create_response.status_code, expected_status_code)
        self.assertEqual(create_response.data['title'], data['title'])
        self.assertEqual(create_response.data['description'], data['description'])
        self.assertTrue('key' in create_response.data)

    def test_blog_post_creation_by_individual_user(self):
        self.authenticate_user(self.user_3.email)
        path = reverse('create-post')
        data = {
            'owner': self.user_3,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': self.user_3.email,
            'phone_number': '0245896732'
        }
        create_response = self.client.post(path=path, data=data)
        expected_status_code = status.HTTP_403_FORBIDDEN
        self.assertEqual(create_response.status_code, expected_status_code)

    def test_blog_post_update_by_staff(self):
        self.authenticate_user(self.user.email)
        update_url = reverse('update-post',
                             kwargs={'pk': self.blog.key})
        data = {
            'title': 'Updated Post',
            'description': 'This is the updated post',
            'phone_number': '0245896736'
        }
        update_response = self.client.put(path=update_url, data=data)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(update_response.status_code, expected_status_code)
        self.assertEqual(update_response.data['title'], data['title'])
        self.assertEqual(update_response.data['description'], data['description'])

    def test_blog_post_update_by_foreigner(self):
        self.authenticate_user(self.bus_user.email)
        update_url = reverse('update-post',
                             kwargs={'pk': self.blog.key})
        data = {
            'title': 'Updated Post',
            'description': 'This is the updated post',
            'phone_number': '0245896736'
        }
        update_response = self.client.put(path=update_url, data=data)
        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(update_response.status_code, expected_status_code)

    def test_get_my_blog_post_list(self):
        self.authenticate_user(self.user.email)
        get_url = reverse('my-posts')
        get_response = self.client.get(path=get_url)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(get_response.status_code, expected_status_code)
        self.assertEqual(get_response.data[0]['title'], self.data['title'])
        self.assertEqual(get_response.data[0]['description'], self.data['description'])

    def test_failed_get_my_blog_post_list_by_foreigner(self):
        self.authenticate_user(self.user_3.email)
        get_url = reverse('my-posts')
        get_response = self.client.get(path=get_url)
        expected_status_code = status.HTTP_403_FORBIDDEN
        self.assertEqual(get_response.status_code, expected_status_code)

    def test_get_my_blog_post_detail(self):
        self.authenticate_user(self.user.email)
        get_url = reverse('detail-my-post', kwargs={'pk': self.blog.key})
        get_response = self.client.get(path=get_url)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(get_response.status_code, expected_status_code)
        self.assertEqual(get_response.data['title'], self.data['title'])
        self.assertEqual(get_response.data['description'], self.data['description'])

    def test_delete_my_blog_post(self):
        self.authenticate_user(self.user.email)
        delete_url = reverse('delete-post', kwargs={'pk': self.blog.key})
        delete_response = self.client.delete(path=delete_url)
        expected_status_code = status.HTTP_204_NO_CONTENT
        self.assertEqual(delete_response.status_code, expected_status_code)

    def test_get_post_list(self):
        get_url = reverse('approved-posts')
        get_response = self.client.get(path=get_url)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(get_response.status_code, expected_status_code)
        self.assertEqual(get_response.data[0]['title'], self.data['title'])
        self.assertEqual(get_response.data[0]['description'], self.data['description'])

    # def test_get_post_detail(self):
    #     get_url = reverse('approved-posts-detail', kwargs={'pk': self.Blog.key})
    #     get_response = self.client.get(path=get_url)
    #     expected_status_code = status.HTTP_200_OK
    #     self.assertEqual(get_response.status_code, expected_status_code)
    #     self.assertEqual(get_response.data['title'], self.data['title'])
    #     self.assertEqual(get_response.data['description'], self.data['description'])
    #     self.assertEqual(get_response.data['category'], self.data['category'])
    #     self.assertEqual(get_response.data['approval_status'], '1')



