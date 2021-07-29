from django.db import models
import smtplib
from email.message import EmailMessage

from accounts.models import CustomUser
from timeofyourlife_v1.my_secrets import GMAIL, GMAIL_PASS


class Feedback(models.Model):
    subject = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(max_length=2000)
    email = models.EmailField(blank=True, null=True)
    user = models.ForeignKey(
        CustomUser,
        related_name='feedback',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def send_notification(self):
        msg = EmailMessage()
        msg['Subject'] = self.subject if self.subject else 'No subject'
        msg['From'] = 'Time of Your Life <noreply@timeofyourlife.io'
        msg['To'] = GMAIL
        msg.set_content(
            f'{self.message}\n\n\nemail: {self.email}\nuser: {self.user}')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL, GMAIL_PASS)
            smtp.send_message(msg)

    def save(self, *args, **kwargs) -> None:
        self.send_notification()
        return super().save(*args, **kwargs)
