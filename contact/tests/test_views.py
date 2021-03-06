from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from unittest.mock import patch

from contact.forms import FeedbackForm, ContactForm
from contact.models import Contact, Feedback

User = get_user_model()


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
@patch('contact.models.Feedback.send_notification')
class FeedbackViewTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('feedback'))

    def test_context_contains_feedback_form(self, mock_notification):
        self.assertIsInstance(
            self.response.context['form'],
            FeedbackForm
        )

    def test_logged_in_user_saves_to_feedback_object(self, mock_notification):
        User.objects.create_user(
            username='testuser',
            day='01',
            month='12',
            year='1995',
            dob='1995-12-01',
            email='test@user.com',
            password='testpass123'
        )
        user = User.objects.first()
        self.client.force_login(user)
        self.client.post(
            reverse('feedback'),
            data={
                'subject': 'my subject',
                'message': 'my feedback message',
                'email': 'my@email.com'
            }
        )
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.user, user)

    def test_non_logged_in_user_doesnt_save_user_to_feedback_object(self, mock_notification):
        self.client.post(
            reverse('feedback'),
            data={
                'subject': 'my subject',
                'message': 'my feedback message',
                'email': 'my@email.com'
            }
        )
        feedback = Feedback.objects.first()
        self.assertFalse(feedback.user)

    def test_post_sends_notificaton(self, mock_notification):
        self.client.post(
            reverse('feedback'),
            data={
                'subject': 'my subject',
                'message': 'my feedback message',
                'email': 'my@email.com'
            }
        )
        self.assertTrue(mock_notification.called)

    def test_post_saves_object_fields(self, mock_notification):
        self.client.post(
            reverse('feedback'),
            data={
                'subject': 'my subject',
                'message': 'my feedback message',
                'email': 'my@email.com'
            }
        )
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.subject, 'my subject')
        self.assertEqual(feedback.message, 'my feedback message')
        self.assertEqual(feedback.email, 'my@email.com')



@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
@patch('contact.models.Contact.send_notification')
class ContactViewTest(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('contact'))

    def test_context_contains_contact_form(self, mock_notification):
        self.assertIsInstance(
            self.response.context['form'],
            ContactForm
        )

    def test_logged_in_user_saves_to_contact_object(self, mock_notification):
        User.objects.create_user(
            username='testuser',
            day='01',
            month='12',
            year='1995',
            dob='1995-12-01',
            email='test@user.com',
            password='testpass123'
        )
        user = User.objects.first()
        self.client.force_login(user)
        self.client.post(
            reverse('contact'),
            data={
                'subject': 'my subject',
                'message': 'my contact message',
                'email': 'my@email.com'
            }
        )
        contact = Contact.objects.first()
        self.assertEqual(contact.user, user)

    def test_non_logged_in_user_doesnt_save_user_to_contact_object(self, mock_notification):
        self.client.post(
            reverse('contact'),
            data={
                'subject': 'my subject',
                'message': 'my contact message',
                'email': 'my@email.com'
            }
        )
        contact = Contact.objects.first()
        self.assertFalse(contact.user)

    def test_post_sends_notificaton(self, mock_notification):
        self.client.post(
            reverse('contact'),
            data={
                'subject': 'my subject',
                'message': 'my contact message',
                'email': 'my@email.com'
            }
        )
        self.assertTrue(mock_notification.called)

    def test_post_saves_object_fields(self, mock_notification):
        self.client.post(
            reverse('contact'),
            data={
                'subject': 'my subject',
                'message': 'my contact message',
                'email': 'my@email.com'
            }
        )
        contact = Contact.objects.first()
        self.assertEqual(contact.subject, 'my subject')
        self.assertEqual(contact.message, 'my contact message')
        self.assertEqual(contact.email, 'my@email.com')
