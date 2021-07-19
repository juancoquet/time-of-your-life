from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()

EVENT_DATE_ERROR = "Event dates must be within a 90-year window starting on your date of birth"


class UserEvent(models.Model):
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
