from django import forms
from datetime import datetime, date
import math


FUTURE_DOB_ERROR = "Date of birth cannot be in the future"

###############
### Helpers ###
###############


def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    else:
        return False



#############
### Forms ###
#############


class DateInput(forms.DateInput):
    input_type = 'date'


class DOBForm(forms.Form):
    dob = forms.DateField(widget=DateInput, label='Date of Birth')

    def clean_dob(self, *args, **kwargs):
        dob_given = self.cleaned_data['dob']
        dob_given = datetime(dob_given.year, dob_given.month, dob_given.day)
        if dob_given >= datetime.today():
            raise forms.ValidationError(FUTURE_DOB_ERROR)
        else:
            return dob_given

    def get_current_year_of_life(self):
        self.full_clean()
        today = date.today()
        dob_given = self.cleaned_data['dob']
        dob_given = date(dob_given.year, dob_given.month, dob_given.day)
        try:
            todays_date_on_birth_year = date(dob_given.year, today.month, today.day)
        except ValueError:  # Today is leap day
            todays_date_on_birth_year = date(dob_given.year, 3, 1)      # Turn into 1st March
        if dob_given > todays_date_on_birth_year:
            current_year = today.year - dob_given.year
        else:
            current_year = (today.year - dob_given.year) + 1
        return current_year

    def get_current_week_no(self):
        self.full_clean()
        today = date.today()
        dob_given = self.cleaned_data['dob']
        dob_given = date(dob_given.year, dob_given.month, dob_given.day)

        try:
            todays_date_on_birth_year = date(dob_given.year, today.month, today.day)
        except ValueError:  # Today is leap day
            todays_date_on_birth_year = date(dob_given.year, 3, 1)  # Turn into 1st March

        if dob_given > todays_date_on_birth_year:
            try:
                todays_date_on_birth_year = date(dob_given.year+1, today.month, today.day)
            except ValueError:  # Today is leap day
                todays_date_on_birth_year = date(dob_given.year+1, 3, 1)  # Turn into 1st March
        days_since_bday = (todays_date_on_birth_year - dob_given).days
        return math.ceil(days_since_bday / 7)

