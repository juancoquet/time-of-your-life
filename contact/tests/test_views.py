from django.test import TestCase
from django.urls import reverse

from contact.forms import FeedbackForm


class FeedbackViewTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('feedback'))

    def test_context_contains_feedback_form(self):
        self.assertIsInstance(
            self.response.context['form'],
            FeedbackForm
        )
