from django.shortcuts import render

from .forms import DOBForm


def home(request):
    dob_form = DOBForm(request.POST or None)
    return render(request, 'home.html', {'dob_form': dob_form})
