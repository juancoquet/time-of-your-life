from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import DOBForm, EventForm


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
    dob_form = DOBForm(data={'dob': dob})
    current_year = dob_form.get_current_year_of_life()

    event_form = EventForm(request.POST or None)
    if request.method == 'POST':
        if event_form.is_valid():
            event_name = event_form.cleaned_data['event_title']
            event_date = event_form.cleaned_data['event_date'].date()
            return redirect(reverse('event', args=[dob, event_name, event_date]))

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
    })
