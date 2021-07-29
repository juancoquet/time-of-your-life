from django.db import models


class Feedback(models.Model):
    subject = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(max_length=2000)
    email = models.EmailField(blank=True, null=True)
