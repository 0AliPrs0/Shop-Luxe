from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    addresses = JSONField(blank=True, null=True, default=list)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return self.username
