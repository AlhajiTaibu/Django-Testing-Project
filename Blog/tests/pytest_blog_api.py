import pytest
from django.urls import reverse
from Blog.models import BlogPost


class TestBlogApi:

    @pytest.fixture
    def set_up(self, create_user):
        user_1 = create_user(username="Staff", email="staff@mail.com", is_staff=True)
        user_2 = create_user(username="Business", email="business@mail.com", is_staff=True)
        user_3 = create_user(username="Normal", email="normal@mail.com")
        data = {
            'owner': user_1,
            'title': 'Third Post',
            'description': 'This is the third post',
            'email': user_1.email,
            'phone_number': '0245896732'
        }
        blog = BlogPost.objects.create(**data)
        yield {
            'staff': user_1,
            'business': user_2,
            'individual': user_3,
            'blog': blog,
            'data': data
        }

    def test_blog_post_creation_by_staff(self, api_client, authenticate, db, set_up):
        path = reverse('create-post')
        staff_user = set_up['staff']
        authenticate(user=staff_user)
        data = {
            'owner': staff_user.email,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': staff_user.email,
            'phone_number': '0245896732'
        }
        create_response = api_client.post(path=path, data=data)
        assert create_response.status_code == 201
        assert create_response.data['title'] == data['title']
        assert create_response.data['description'] == data['description']
        assert 'key' in create_response.data

    def test_blog_post_creation_by_individual_user(self, api_client, authenticate, db, set_up):
        path = reverse('create-post')
        individual_user = set_up['individual']
        authenticate(user=individual_user)
        data = {
            'owner': individual_user,
            'title': 'First Post',
            'description': 'This is the first post',
            'email': individual_user.email,
            'phone_number': '0245896732'
        }
        create_response = api_client.post(path=path, data=data)
        expected_status_code = 403
        assert create_response.status_code == expected_status_code

    def test_blog_post_update_by_staff(self, api_client, authenticate, db, set_up):
        blog = set_up['blog']
        update_url = reverse('update-post',
                             kwargs={'pk': blog.key})
        staff_user = set_up['staff']
        authenticate(user=staff_user)
        data = {
            'title': 'Updated Post',
            'description': 'This is the updated post',
            'phone_number': '0245896736'
        }
        update_response = api_client.put(path=update_url, data=data)
        expected_status_code = 200
        assert update_response.status_code == expected_status_code
        assert update_response.data['title'] == data['title']
        assert update_response.data['description'] == data['description']

    def test_blog_post_update_by_foreigner(self, api_client, authenticate, db, set_up):
        blog = set_up['blog']
        update_url = reverse('update-post',
                             kwargs={'pk': blog.key})
        business_user = set_up['business']
        authenticate(user=business_user)
        data = {
            'title': 'Updated Post',
            'description': 'This is the updated post',
            'phone_number': '0245896736'
        }
        update_response = api_client.put(path=update_url, data=data)
        expected_status_code = 404
        assert update_response.status_code == expected_status_code

    def test_get_my_blog_post_list(self, api_client, authenticate, db, set_up):
        data = set_up['data']
        staff_user = set_up['staff']
        authenticate(user=staff_user)
        get_url = reverse('my-posts')
        get_response = api_client.get(path=get_url)
        expected_status_code = 200
        assert get_response.status_code == expected_status_code
        assert get_response.data[0]['title'] == data['title']
        assert get_response.data[0]['description'] == data['description']

    def test_failed_get_my_blog_post_list_by_foreigner(self, api_client, authenticate, db, set_up):
        individual_user = set_up['individual']
        authenticate(user=individual_user)
        get_url = reverse('my-posts')
        get_response = api_client.get(path=get_url)
        expected_status_code = 403
        assert get_response.status_code == expected_status_code

    def test_get_my_blog_post_detail(self, api_client, authenticate, db, set_up):
        staff_user = set_up['staff']
        blog = set_up['blog']
        data = set_up['data']
        authenticate(user=staff_user)
        get_url = reverse('detail-my-post', kwargs={'pk': blog.key})
        get_response = api_client.get(path=get_url)
        expected_status_code = 200
        assert get_response.status_code == expected_status_code
        assert get_response.data['title'] == data['title']
        assert get_response.data['description'] == data['description']

    def test_delete_my_blog_post(self, api_client, authenticate, db, set_up):
        blog = set_up['blog']
        staff_user = set_up['staff']
        authenticate(user=staff_user)
        delete_url = reverse('delete-post', kwargs={'pk': blog.key})
        delete_response = api_client.delete(path=delete_url)
        expected_status_code = 204
        assert delete_response.status_code == expected_status_code

    def test_get_post_list(self, api_client, authenticate, db, set_up):
        data = set_up['data']
        get_url = reverse('approved-posts')
        get_response = api_client.get(path=get_url)
        expected_status_code = 200
        assert get_response.status_code == expected_status_code
        assert get_response.data[0]['title'] == data['title']
        assert get_response.data[0]['description'] == data['description']
