from django.test import TestCase

from contact.forms import FeedbackForm
from contact.models import Feedback


class FeedbackFormTest(TestCase):

    def test_valid_form_creates_new_object(self):
        form = FeedbackForm(
            subject='Test subject',
            message='This is my feedback message',
            email='test@email.com',
        )
        form.save()
        self.assertEqual(len(Feedback.objects.all()), 1)

    def test_email_not_required(self):
        form = FeedbackForm(
            subject='Test subject',
            message='This is my feedback message',
            email='',
        )
        self.assertTrue(form.is_valid())

    def test_subject_not_required(self):
        form = FeedbackForm(
            subject='',
            message='This is my feedback message',
            email='test@email.com',
        )
        self.assertTrue(form.is_valid())

    def test_message_is_required(self):
        form = FeedbackForm(
            subject='Test subject',
            message='',
            email='test@email.com',
        )
        self.assertFalse(form.is_valid())

    # TODO: Test logged in user saves to fedback object
    # TODO: Test non-logged in user doesn't save user to object
