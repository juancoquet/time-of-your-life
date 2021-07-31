from django.urls.base import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .forms import FeedbackForm, ContactForm

FEEDBACK_MESSAGE = "Thanks for your feedback!"


class FeedbackView(CreateView):
    form_class = FeedbackForm
    template_name = 'feedback.html'
    success_url = reverse_lazy('feedback')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.user.is_authenticated:
            self.object.user = self.request.user
        messages.success(
            self.request, FEEDBACK_MESSAGE, extra_tags='custom')
        return super().form_valid(form)


class ContactView(CreateView):
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.user.is_authenticated:
            self.object.user = self.request.user
        messages.success(
            self.request, 'Message sent', extra_tags='custom')
        return super().form_valid(form)
