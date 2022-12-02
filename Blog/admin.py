from django.contrib import admin
from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    model = BlogPost
    list_display = [
        'title',
        'description',
        'created_at',
        'edited_at',
        'owner',
        'expiry_date',
    ]


admin.site.register(BlogPost, BlogPostAdmin)
