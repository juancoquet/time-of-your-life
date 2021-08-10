from datetime import date
from django import forms
import math

from .models import UserEvent


FUTURE_DOB_ERROR = "Date of birth cannot be in the future"

PAST_DOB_ERROR = "Date of birth cannot be more that 90 years ago"

EVENT_DATE_ERROR = "Event dates must be within a 90-year window starting on your date of birth"

DUPLICATE_EVENT_ERROR = "This event already exists"

INVALID_DATE_ERROR = "Please enter a valid date"

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
        minus_90 = date(today.year-90, today.month, today.day)
    except ValueError:
        minus_90 = date(today.year-90, 3, 1)
    return minus_90


#############
### Forms ###
#############


class DateInput(forms.DateInput):
    input_type = 'date'


class DOBForm(forms.Form):
    day = forms.IntegerField(min_value=1, max_value=31)
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.IntegerField(min_value=1, max_value=9999)

    day.widget.attrs.update({
        'class': 'input input--int banner__input',
        'placeholder': 'DD',
    })
    month.widget.attrs.update(
        {'class': 'input input--int banner__input', 'placeholder': 'MM'})
    year.widget.attrs.update(
        {'class': 'input input--int banner__input', 'placeholder': 'YYYY'})

    def clean_year(self, *args, **kwargs):
        day_given = int(self['day'].data)
        month_given = int(self['month'].data)
        year_given = int(self['year'].data)
        try:
            dob_given = date(year_given, month_given, day_given)
            if dob_given >= date.today():
                self.errors['year'] = FUTURE_DOB_ERROR
            if dob_given < get_today_minus_90_years():
                self.errors['year'] = PAST_DOB_ERROR
            else:
                return year_given
        except ValueError:
            self.errors['year'] = INVALID_DATE_ERROR

    def is_valid(self) -> bool:
        day_given = int(self['day'].data)
        month_given = int(self['month'].data)
        year_given = int(self['year'].data)
        try:
            date(year_given, month_given, day_given)
        except ValueError:
            self.errors['year'] = INVALID_DATE_ERROR
            return False
        return super().is_valid()

    def get_current_year_of_life(self):
        self.full_clean()
        day_given = self.cleaned_data['day']
        month_given = self.cleaned_data['month']
        year_given = self.cleaned_data['year']
        dob_given = date(year_given, month_given, day_given)

        todays_date_on_birth_year = get_todays_date_on_birth_year(dob_given)

        today = date.today()
        if dob_given > todays_date_on_birth_year:
            current_year = today.year - dob_given.year
        else:
            current_year = (today.year - dob_given.year) + 1

        return current_year

    def get_current_week_no(self):
        self.full_clean()
        day_given = self.cleaned_data['day']
        month_given = self.cleaned_data['month']
        year_given = self.cleaned_data['year']
        dob_given = date(year_given, month_given, day_given)

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
    day = forms.IntegerField(min_value=1, max_value=31)
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.IntegerField(min_value=1, max_value=9999)

    event_title.widget.attrs.update({
        'class': 'input',
        'placeholder': 'Event name'
    })
    day.widget.attrs.update({
        'class': 'input input--int',
        'placeholder': 'DD',
    })
    month.widget.attrs.update(
        {'class': 'input input--int', 'placeholder': 'MM'})
    year.widget.attrs.update(
        {'class': 'input input--int', 'placeholder': 'YYYY'})

    def clean_year(self, *args, **kwargs):
        day_given = int(self['day'].data)
        month_given = int(self['month'].data)
        year_given = int(self['year'].data)
        try:
            date_given = date(year_given, month_given, day_given)
            if date_given < get_today_minus_90_years():
                self.errors['year'] = EVENT_DATE_ERROR
            else:
                return year_given
        except ValueError:
            self.errors['year'] = INVALID_DATE_ERROR

    def is_valid(self) -> bool:
        day_given = int(self['day'].data)
        month_given = int(self['month'].data)
        year_given = int(self['year'].data)
        try:
            date(year_given, month_given, day_given)
        except ValueError:
            self.errors['year'] = INVALID_DATE_ERROR
            return False
        return super().is_valid()


class UserEventForm(forms.ModelForm):

    class Meta:
        model = UserEvent
        fields = ['event_name', 'day', 'month', 'year']
        widgets = {
            'event_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Event name'
            }),
            'day': forms.NumberInput(attrs={
                'class': 'input input--int',
                'placeholder': 'DD',
            }),
            'month': forms.NumberInput(attrs={
                'class': 'input input--int',
                'placeholder': 'MM',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'input input--int',
                'placeholder': 'YYYY',
            }),
        }

    def save(self, commit=True):
        event = super().save(commit=False)
        day_given = self.cleaned_data['day']
        month_given = self.cleaned_data['month']
        year_given = self.cleaned_data['year']
        event.event_date = date(year_given, month_given, day_given)
        if commit:
            event.save_event()
        return event

    def show_event_date_error(self):
        self.errors['year'] = EVENT_DATE_ERROR

    def show_unique_restraint_error(self):
        self.errors['year'] = DUPLICATE_EVENT_ERROR

    def year_field_within_range(self):
        if int(self['year'].data) > 2999:
            self.errors['year'] = EVENT_DATE_ERROR
            return False
        return True

    def is_valid(self) -> bool:
        day_given = int(self['day'].data)
        month_given = int(self['month'].data)
        year_given = int(self['year'].data)
        try:
            date(year_given, month_given, day_given)
        except ValueError:
            self.errors['year'] = INVALID_DATE_ERROR
            return False
        if self.year_field_within_range():
            return super().is_valid()
        return False
