from django import forms
from datetime import datetime, date
import math


FUTURE_DOB_ERROR = "Date of birth cannot be in the future"

PAST_DOB_ERROR = "Date of birth cannot be more that 90 years ago"

EVENT_DATE_ERROR = "Event dates must be within a 90-year window starting on your date of birth"

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


def get_todays_date_on_birth_year(dob):
    today = date.today()
    try:
        todays_date_on_birth_year = date(dob.year, today.month, today.day)
    except ValueError:  # Today is leap day
        todays_date_on_birth_year = date(dob.year, 3, 1)  # Turn into 1st March
    return todays_date_on_birth_year


def get_today_minus_90_years():
    today = date.today()
    try:
        minus_90 = datetime(today.year-90, today.month, today.day)
    except ValueError:
        minus_90 = datetime(today.year-90, 3, 1)
    return minus_90


#############
### Forms ###
#############


class DateInput(forms.DateInput):
    input_type = 'date'


class DOBForm(forms.Form):
    dob = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={"class": "datepicker"})
    )

    def clean_dob(self, *args, **kwargs):
        dob_given = self.cleaned_data['dob']
        dob_given = datetime(dob_given.year, dob_given.month, dob_given.day)
        if dob_given >= datetime.today():
            raise forms.ValidationError(FUTURE_DOB_ERROR)
        if dob_given < get_today_minus_90_years():
            raise forms.ValidationError(PAST_DOB_ERROR)
        else:
            return dob_given.date()

    def get_current_year_of_life(self):
        self.full_clean()
        dob_given = self.cleaned_data['dob']
        dob_given = date(dob_given.year, dob_given.month, dob_given.day)

        todays_date_on_birth_year = get_todays_date_on_birth_year(dob_given)

        today = date.today()
        if dob_given > todays_date_on_birth_year:
            current_year = today.year - dob_given.year
        else:
            current_year = (today.year - dob_given.year) + 1

        return current_year

    def get_current_week_no(self):
        self.full_clean()
        dob_given = self.cleaned_data['dob']
        dob_given = date(dob_given.year, dob_given.month, dob_given.day)

        todays_date_on_birth_year = get_todays_date_on_birth_year(dob_given)

        if dob_given > todays_date_on_birth_year:
            today = date.today()
            try:
                todays_date_on_birth_year = date(
                    dob_given.year+1, today.month, today.day)
            except ValueError:  # Today is leap day
                todays_date_on_birth_year = date(
                    dob_given.year+1, 3, 1)  # Turn into 1st March

        days_since_bday = (todays_date_on_birth_year - dob_given).days
        week_no = math.ceil(days_since_bday / 7)
        if week_no == 53:
            week_no = 52
        if week_no == 0:
            week_no = 1
        return week_no

    @property
    def weeks_passed(self):
        full_years_passed = self.get_current_year_of_life() - 1
        full_weeks_passed_this_year = self.get_current_week_no() - 1
        total_weeks_passed = (full_years_passed*52) + \
            full_weeks_passed_this_year
        return range(1, total_weeks_passed + 1)


class EventForm(forms.Form):
    event_title = forms.CharField(max_length='100')
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "datepicker"})
    )

    def clean_event_date(self, *args, **kwargs):
        date_given = self.cleaned_data['event_date']
        date_given = datetime(
            date_given.year, date_given.month, date_given.day)

        if date_given < get_today_minus_90_years():
            raise forms.ValidationError(EVENT_DATE_ERROR)
        else:
            return date_given.date()
