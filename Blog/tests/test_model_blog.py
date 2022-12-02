from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from Blog.models import BlogPost


class TestBlogPostModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create_user(
            username="Luke",
            email="staff@mail.com", password="pAssw0rd1"
        )
        cls.user_1.is_activated = True
        cls.user_1.is_active = True
        cls.user_1.is_staff = True
        cls.user_1.save()

        cls.user_2 = get_user_model().objects.create_user(
            username="Business",
            email="business@mail.com", password="pAssw0rd1"
        )
        cls.user_2.is_activated = True
        cls.user_2.is_active = True
        cls.user_2.is_staff = True
        cls.user_2.save()

        cls.user_3 = get_user_model().objects.create_user(
            username="Normal",
            email="user@mail.com", password="pAssw0rd1"
        )
        cls.user_3.is_activated = True
        cls.user_3.is_active = True
        cls.user_3.save()

    def test_create_blog_post(self):
        data = {
            'owner': self.user_1,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': self.user_1.email,
            'phone_number': '0245896732'
        }
        blog_post = BlogPost.objects.create(**data)
        self.assertEqual(blog_post.title, data['title'])

    def test_failed_create_blog_post_by_individual_user(self):
        data = {
            'owner': self.user_3,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': self.user_3.email,
            'phone_number': '0245896732'
        }
        with self.assertRaises(ValidationError):
            BlogPost.objects.create(**data)

    def test_create_multiple_blog_post(self):
        data_1 = {
            'owner': self.user_1,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': self.user_1.email,
            'phone_number': '0245896732'
        }

        data_2 = {
            'owner': self.user_2,
            'title': 'Third Post',
            'description': 'This is the third post',
            'email': self.user_2.email,
            'phone_number': '0245896732'
        }
        blog_post_1 = BlogPost.objects.create(**data_1)
        blog_post_2 = BlogPost.objects.create(**data_2)
        self.assertEqual(blog_post_1.title, data_1['title'])
        self.assertEqual(blog_post_2.title, data_2['title'])
