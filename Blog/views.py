from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from assets.permissions import IsStaffUser
from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostAPI(generics.ListCreateAPIView):
    queryset = BlogPost.objects
    serializer_class = BlogPostSerializer
    permission_classes = [IsStaffUser, ]
    authentication_classes = [JWTAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class BlogPostRetrieveUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects
    serializer_class = BlogPostSerializer
    authentication_classes = [JWTAuthentication, ]

    def get_queryset(self):
        owner = self.request.user
        return self.queryset.filter(owner=owner)


class BlogPostList(generics.ListAPIView):
    queryset = BlogPost.objects
    serializer_class = BlogPostSerializer
    authentication_classes = [JWTAuthentication, ]

