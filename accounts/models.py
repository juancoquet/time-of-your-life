from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, blank=False, unique=True)
    dob = models.DateField(blank=False)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dob', 'username']
