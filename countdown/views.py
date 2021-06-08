from django.shortcuts import render

from .forms import DOBForm


def home(request):
    dob_form = DOBForm()
    return render(request, 'home.html', {'dob_form': dob_form})
