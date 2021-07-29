from django.urls import path

from .views import FeedbackView


urlpatterns = [
    path('feedback/', FeedbackView.as_view(), name='feedback'),
]
