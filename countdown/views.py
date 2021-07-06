import math

from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import DOBForm, EventForm


###############
### Helpers ###
###############

def get_event_year_of_life(event_date, dob):
    try:
        event_date_on_birth_year = date(
            dob.year, event_date.month, event_date.day)
    except ValueError:  # Event day is leap day
        event_date_on_birth_year = date(dob.year, 3, 1)  # Turn into 1st March

    if event_date_on_birth_year < dob.date():
        event_year_of_life = event_date.year - dob.year
    else:
        event_year_of_life = (event_date.year - dob.year) + 1

    return event_year_of_life


def get_event_week_number(event_date, dob):
    try:
        event_date_on_birth_year = date(
            dob.year, event_date.month, event_date.day)
    except ValueError:  # Event day is leap day
        event_date_on_birth_year = date(dob.year, 3, 1)  # Turn into 1st March
    if dob.date() < event_date_on_birth_year:
        event_date_on_birth_year = date(
            event_date_on_birth_year.year+1,
            event_date_on_birth_year.month,
            event_date_on_birth_year.day
        )

    days_passed = (dob.date() - event_date_on_birth_year).days
    week_no = math.ceil(days_passed / 7)
    if week_no == 53:
        week_no = 52
    if week_no == 0:
        week_no = 1
    return week_no


#############
### Views ###
#############


def home(request):
    dob_form = DOBForm(request.POST or None)
    if request.method == 'POST':
        if dob_form.is_valid():
            dob = dob_form.cleaned_data['dob'].date()
            return redirect(f'grid/{dob}')
    return render(request, 'home.html', {'dob_form': dob_form})


def grid(request, dob, event_name=None, event_date=None):
    if not DOBForm(data={'dob': dob}).is_valid():
        return redirect('/')

    event_form = EventForm(request.POST or None)
    if request.method == 'POST':
        if event_form.is_valid():
            event_name = event_form.cleaned_data['event_title']
            event_date = event_form.cleaned_data['event_date'].date()
            return redirect(reverse('event', args=[dob, event_name, event_date]))

    dob_form = DOBForm(data={'dob': dob})
    current_year = dob_form.get_current_year_of_life()

    if event_name and event_date:
        event = EventForm(
            data={'event_title': event_name, 'event_date': event_date})
        event.is_valid()
        event_year_of_life = get_event_year_of_life(
            event.cleaned_data['event_date'], dob_form.cleaned_data['dob'])
        event_week_no = get_event_week_number(
            event.cleaned_data['event_date'], dob_form.cleaned_data['dob'])
    else:
        event_year_of_life = None
        event_week_no = None

    return render(request, 'grid.html', {
        'years_passed': range(1, current_year),
        'current_year': current_year,
        'future_years': range(current_year + 1, 91),
        'full_year_weeks': range(1, 53),
        'weeks_passed_this_yr': range(1, dob_form.get_current_week_no()),
        'current_week': dob_form.get_current_week_no(),
        'weeks_left_this_yr': range(dob_form.get_current_week_no() + 1, 53),
        'event_form': event_form,
        'date_of_birth': dob,
        'event_year': event_year_of_life,
        'event_week': event_week_no,
    })
