from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=50, blank=False, null=False, unique=True)
    dob = models.DateField(blank=False)
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dob', 'username']

    def _get_todays_date_on_birth_year(self):
        today = date.today()
        try:
            todays_date_on_birth_year = date(
                self.dob.year, today.month, today.day)
        except ValueError:  # Today is leap day
            todays_date_on_birth_year = date(
                self.dob.year, 3, 1)  # Turn into 1st March
        return todays_date_on_birth_year

    @property
    def current_year(self):
        todays_date_on_birth_year = self._get_todays_date_on_birth_year()

        today = date.today()
        if self.dob > todays_date_on_birth_year:
            current_year = today.year - self.dob.year
        else:
            current_year = (today.year - self.dob.year) + 1

        return current_year
