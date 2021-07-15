from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserEvent(models.Model):
    event_name = models.CharField(max_length=100, blank=False, null=False)
    event_date = models.DateField(blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
