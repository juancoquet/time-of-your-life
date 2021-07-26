from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import request
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account_login')
    template_name = 'account/signup.html'


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = CustomUserChangeForm
    login_url = reverse_lazy('account_login')
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != self.request.user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('profile', kwargs={'pk': self.request.user.username})

    # TODO: Catch event out of bounds on post
