from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from math import ceil
import uuid

User = get_user_model()

EVENT_DATE_ERROR = "Event dates must be within a 90-year window starting on your date of birth"


class UserEvent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    event_name = models.CharField(max_length=100, blank=False, null=False)
    event_date = models.DateField(blank=False, null=False)
    owner = models.ForeignKey(
        User, related_name='events', on_delete=models.CASCADE)

    ###############
    ### Methods ###
    ###############

    def _event_is_within_90_years_of_dob(self):
        try:
            dob_plus_90 = date(self.owner.dob.year+90,
                               self.owner.dob.month,
                               self.owner.dob.day)
        except ValueError:      # dob is leap day
            dob_plus_90 = date(self.owner.dob.year+90, 3,
                               1)    # turn into 1st March
        if self.event_date > dob_plus_90 or self.event_date < self.owner.dob:
            return False
        else:
            return True

    def my_clean(self):
        if isinstance(self.event_date, str):
            year, month, day = (int(x) for x in self.event_date.split('-'))
            self.event_date = date(year, month, day)
        if not self._event_is_within_90_years_of_dob():
            raise ValidationError(EVENT_DATE_ERROR)

    def is_valid(self):
        try:
            self.my_clean()
            return True
        except ValidationError:
            return False

    def save_event(self):
        if self.is_valid():
            self.save()
        else:
            raise(ValidationError(EVENT_DATE_ERROR))

    @property
    def index(self):
        """Gets the year and week number for the event object in relation to the owner's
        date of birth.

        Returns:
            tuple: (year_number, week_number)
        """
        self.my_clean()
        try:
            event_date_on_birth_yr = date(self.owner.dob.year,
                                          self.event_date.month,
                                          self.event_date.day)
        except ValueError:
            event_date_on_birth_yr = date(self.owner.dob.year, 3, 1)
        if self.owner.dob > event_date_on_birth_yr:
            year_no = self.event_date.year - self.owner.dob.year
            event_date_on_birth_yr = date(
                event_date_on_birth_yr.year+1,
                event_date_on_birth_yr.month,
                event_date_on_birth_yr.day
            )
        else:
            year_no = (self.event_date.year - self.owner.dob.year) + 1

        days_since_bday = (event_date_on_birth_yr - self.owner.dob).days
        week_no = ceil(days_since_bday / 7)
        if week_no == 53:
            week_no = 52
        if week_no == 0:
            week_no = 1
        return (year_no, week_no)

    def get_edit_url(self):
        return reverse("event_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("event_delete", kwargs={"pk": self.pk})
