import pytest
from Blog.models import BlogPost


class TestBlogModel:

    @pytest.mark.django_db
    def test_create_blog_post(self, user_factory):
        user = user_factory(is_staff=True)
        data = {
            'owner': user,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': user.email,
            'phone_number': '0245896732'
        }
        blog_post = BlogPost.objects.create(**data)
        assert blog_post.title == data['title']

    @pytest.mark.django_db
    def test_create_multiple_blog_post(self, user_factory):
        user_1 = user_factory(is_staff=True)
        data_1 = {
            'owner': user_1,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': user_1.email,
            'phone_number': '0245896732'
        }

        data_2 = {
            'owner': user_1,
            'title': 'Third Post',
            'description': 'This is the third post',
            'email': user_1.email,
            'phone_number': '0245896732'
        }
        blog_post_1 = BlogPost.objects.create(**data_1)
        blog_post_2 = BlogPost.objects.create(**data_2)
        assert blog_post_1.title == data_1['title']
        assert blog_post_2.title == data_2['title']
