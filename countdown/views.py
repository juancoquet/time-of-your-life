from django.shortcuts import render, redirect

from .forms import DOBForm


def home(request):
    dob_form = DOBForm(request.POST or None)
    if request.method == 'POST':
        if dob_form.is_valid():
            dob = dob_form.cleaned_data['dob'].date()
            return redirect(f'grid/{dob}')
    return render(request, 'home.html', {'dob_form': dob_form})


def grid(request, dob):
    if not DOBForm(data={'dob': dob}).is_valid():
        return redirect('/')
    return render(request, 'grid.html', {'year_list': range(90)})
