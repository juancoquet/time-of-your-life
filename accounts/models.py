import math
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

    ###############
    ### Mehtods ###
    ###############

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

    @property
    def years_passed(self):
        return range(1, self.current_year)

    @property
    def future_years(self):
        return range(self.current_year + 1, 91)

    @property
    def current_week(self):
        todays_date_on_birth_year = self._get_todays_date_on_birth_year()
        if self.dob > todays_date_on_birth_year:
            today = date.today()
            try:
                todays_date_on_birth_year = date(
                    self.dob.year+1, today.month, today.day)
            except ValueError:  # Today is leap day
                todays_date_on_birth_year = date(
                    self.dob.year+1, 3, 1)  # Turn into 1st March

        days_since_bday = (todays_date_on_birth_year - self.dob).days
        week_no = math.ceil(days_since_bday / 7)
        if week_no == 53:
            week_no = 52
        if week_no == 0:
            week_no = 1
        return week_no

    @property
    def weeks_passed_this_yr(self):
        return range(1, self.current_week)

    @property
    def weeks_left_this_yr(self):
        return range(self.current_week + 1, 53)

    # TODO: Create week class which contains yr/no in a coordinate-like system
    # TODO: Create calendar @property to generate weeks iter
