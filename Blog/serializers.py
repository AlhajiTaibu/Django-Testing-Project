from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'key',
            'title', 'description', 'phone_number',
            'email', 'created_at',
            'edited_at', 'reviewed_at', 'expiry_date',
        ]
        extra_kwargs = {
            'owner': {'required': False},
        }
