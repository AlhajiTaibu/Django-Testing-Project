import pytest

from Blog.models import BlogPost


class TestBlogModel:

    @pytest.mark.django_db
    def test_create_blog_post(self, create_user):
        user = create_user(username="Luke", email="staff@mail.com", is_staff=True)
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
    def test_create_multiple_blog_post(self, create_user):
        user_1 = create_user(username="Luke", email="staff@mail.com", is_staff=True)
        user_2 = create_user(username="PJ", email="pj@mail.com", is_staff=True)
        data_1 = {
            'owner': user_1,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': user_1.email,
            'phone_number': '0245896732'
        }

        data_2 = {
            'owner': user_2,
            'title': 'Third Post',
            'description': 'This is the third post',
            'email': user_2.email,
            'phone_number': '0245896732'
        }
        blog_post_1 = BlogPost.objects.create(**data_1)
        blog_post_2 = BlogPost.objects.create(**data_2)
        assert blog_post_1.title == data_1['title']
        assert blog_post_2.title == data_2['title']

    @pytest.mark.django_db
    def test_failed_create_blog_post_by_individual_user(self, create_user):
        user = create_user(username="individual", email="individual@mail.com")
        data = {
            'owner': user,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': user.email,
            'phone_number': '0245896732'
        }
        with pytest.raises(Exception) as exec_info:
            BlogPost.objects.create(**data)
        assert exec_info.value.args[0] == "Only Staff users are allowed to create or edit post"
