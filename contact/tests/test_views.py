from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from contact.forms import FeedbackForm


@patch('contact.models.Feedback.send_notification')
class FeedbackViewTest(TestCase):

    def setUp(self, mock_notification):
        self.response = self.client.get(reverse('feedback'))

    def test_context_contains_feedback_form(self, mock_notification):
        self.assertIsInstance(
            self.response.context['form'],
            FeedbackForm
        )

# TODO: Test logged in user saves to fedback object
# TODO: Test non-logged in user doesn't save user to object
