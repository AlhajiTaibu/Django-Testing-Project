from django.urls import path
from .views import (
    BlogPostAPI,
    BlogPostRetrieveUpdate, BlogPostList,
)

urlpatterns = [
    path(
        'my-posts',
        BlogPostAPI.as_view(),
        name='my-posts'
    ),
    path(
        'create-post',
        BlogPostAPI.as_view(),
        name='create-post'
    ),
    path(
        'update-post/<pk>/',
        BlogPostRetrieveUpdate.as_view(),
        name='update-post'
    ),
    path(
        'my-posts/<pk>/',
        BlogPostRetrieveUpdate.as_view(),
        name='detail-my-post'
    ),
    path(
        'delete-post/<pk>/',
        BlogPostRetrieveUpdate.as_view(),
        name='delete-post'
    ),
    path(
        'posts',
        BlogPostList.as_view(),
        name='approved-posts'
    ),
    # path(
    #     'posts/<pk>/',
    #     BlogPostRetreive.as_view(),
    #     name='approved-posts-detail'
    # ),
]
