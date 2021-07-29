from django.shortcuts import render
from django.views.generic import CreateView

from .forms import FeedbackForm


class FeedbackView(CreateView):
    form_class = FeedbackForm
