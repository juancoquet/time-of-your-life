from django.urls.base import reverse_lazy
from django.views.generic import CreateView

from .forms import FeedbackForm


class FeedbackView(CreateView):
    form_class = FeedbackForm
    template_name = 'feedback.html'
    success_url = reverse_lazy('feedback')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.user.is_authenticated:
            self.object.user = self.request.user
        return super().form_valid(form)
