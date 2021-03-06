from django.test import TestCase
from unittest.mock import patch

from contact.forms import FeedbackForm, ContactForm
from contact.models import Feedback, Contact


@patch('contact.models.Feedback.send_notification')
class FeedbackFormTest(TestCase):

    def test_valid_form_creates_new_object(self, mock_notification):
        form = FeedbackForm(
            data={
                'subject': 'Test subject',
                'message': 'This is my feedback message',
                'email': 'test@email.com'
            }
        )
        form.save()
        self.assertEqual(len(Feedback.objects.all()), 1)

    def test_email_not_required(self, mock_notification):
        form = FeedbackForm(
            data={
                'subject': 'Test subject',
                'message': 'This is my feedback message',
                'email': None
            }
        )
        self.assertTrue(form.is_valid())

    def test_subject_not_required(self, mock_notification):
        form = FeedbackForm(
            data={
                'subject': None,
                'message': 'This is my feedback message',
                'email': 'test@email.com'
            }
        )
        self.assertTrue(form.is_valid())

    def test_message_is_required(self, mock_notification):
        form = FeedbackForm(
            data={
                'subject': 'Test subject',
                'message': None,
                'email': 'test@email.com'
            }
        )
        self.assertFalse(form.is_valid())


@patch('contact.models.Contact.send_notification')
class ContactFormTest(TestCase):

    def test_valid_form_creates_new_object(self, mock_notification):
        form = ContactForm(
            data={
                'subject': 'Test subject',
                'message': 'This is my feedback message',
                'email': 'test@email.com'
            }
        )
        form.save()
        self.assertEqual(len(Contact.objects.all()), 1)

    def test_email_required(self, mock_notification):
        form = ContactForm(
            data={
                'subject': 'Test subject',
                'message': 'This is my feedback message',
                'email': None
            }
        )
        self.assertFalse(form.is_valid())

    def test_subject_not_required(self, mock_notification):
        form = ContactForm(
            data={
                'subject': None,
                'message': 'This is my feedback message',
                'email': 'test@email.com'
            }
        )
        self.assertTrue(form.is_valid())

    def test_message_is_required(self, mock_notification):
        form = ContactForm(
            data={
                'subject': 'Test subject',
                'message': None,
                'email': 'test@email.com'
            }
        )
        self.assertFalse(form.is_valid())
