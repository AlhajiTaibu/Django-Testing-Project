from datetime import datetime
from uuid import uuid4, uuid1

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class BlogPost(models.Model):
    key = models.CharField(
        max_length=32,
        primary_key=True,
        editable=False
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blogs"
    )
    title = models.CharField(
        max_length=100
    )
    description = models.TextField()
    phone_number = models.CharField(
        max_length=20,
        blank=True
    )
    email = models.EmailField(
        max_length=100,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    edited_at = models.DateTimeField(
        blank=True,
        null=True
    )
    reviewed_at = models.DateTimeField(
        blank=True,
        null=True
    )
    expiry_date = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-edited_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = generate_key(BlogPost)
        if not self.owner.is_staff:
            raise ValidationError('Only Staff users are allowed to create or edit post')
        if self.edited_at == '':
            self.edited_at = self.created_at
        else:
            self.edited_at = datetime.now()
        super().save(*args, **kwargs)


def generate_key(model, length=32, method="uuid4"):
    """
    length needs to be <= 32
    """
    generator = {"uuid1": uuid1, "uuid4": uuid4}
    key = generator[method]().hex[:length]
    while model.objects.filter(key=key).exists():
        key = generator[method]().hex[:length]
    return key
