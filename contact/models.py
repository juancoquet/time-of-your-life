from django.db import models
from django.template.defaultfilters import truncatechars
import smtplib
from email.message import EmailMessage

from accounts.models import CustomUser

from environs import Env

env = Env()
env.read_env()

try:
    from timeofyourlife_v1.my_secrets import (GMAIL, MY_EMAIL_HOST, MY_EMAIL_HOST_USER,
                                            MY_EMAIL_HOST_PASSWORD, MY_EMAIL_PORT)
except ModuleNotFoundError:
    MY_EMAIL_HOST = env('MY_EMAIL_HOST')
    MY_EMAIL_HOST_USER = env('MY_EMAIL_HOST_USER')
    MY_EMAIL_HOST_PASSWORD = env('MY_EMAIL_HOST_PASSWORD')
    MY_EMAIL_PORT = env.int('MY_EMAIL_PORT')
    GMAIL = env('GMAIL')
    


class Feedback(models.Model):
    subject = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(max_length=2000)
    email = models.EmailField(blank=True, null=True)
    user = models.ForeignKey(
        CustomUser,
        related_name='feedback',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = 'Feedback'

    @property
    def short_msg(self):
        return truncatechars(self.message, 100)

    def send_notification(self):
        msg = EmailMessage()
        msg['Subject'] = f'Feedback: {self.subject}' if self.subject else 'Feedback: No subject'
        msg['From'] = 'Time of Your Life <noreply@timeofyourlife.io>'
        msg['To'] = GMAIL
        msg.set_content(
            f'{self.message}\n\n\nemail: {self.email}\nuser: {self.user}')

        with smtplib.SMTP(MY_EMAIL_HOST, MY_EMAIL_PORT) as smtp:
            smtp.login(MY_EMAIL_HOST_USER, MY_EMAIL_HOST_PASSWORD)
            smtp.send_message(msg)

    def save(self, *args, **kwargs) -> None:
        self.send_notification()
        return super().save(*args, **kwargs)


class Contact(models.Model):
    subject = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(max_length=2000)
    email = models.EmailField()
    user = models.ForeignKey(
        CustomUser,
        related_name='contact',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = 'Contact'

    @property
    def short_msg(self):
        return truncatechars(self.message, 100)

    def send_notification(self):
        msg = EmailMessage()
        msg['Subject'] = f'Contact: {self.subject}' if self.subject else 'Contact: No subject'
        msg['From'] = 'Time of Your Life <noreply@timeofyourlife.io>'
        msg['To'] = GMAIL
        msg.set_content(
            f'{self.message}\n\n\nemail: {self.email}\nuser: {self.user}')

        with smtplib.SMTP(MY_EMAIL_HOST, MY_EMAIL_PORT) as smtp:
            smtp.login(MY_EMAIL_HOST_USER, MY_EMAIL_HOST_PASSWORD)
            smtp.send_message(msg)

    def save(self, *args, **kwargs) -> None:
        self.send_notification()
        return super().save(*args, **kwargs)
