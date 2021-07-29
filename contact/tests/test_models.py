from django.test import TestCase

from contact.models import Feedback


class FeedbackModelTest(TestCase):

    def test_valid_feedback(self):
        Feedback.objects.create(
            subject='Test feedback',
            message='my feedback message',
            email='test@email.com'
        )
        self.assertEqual(len(Feedback.objects.all()), 1)

    def test_subject_not_required(self):
        Feedback.objects.create(
            subject=None,
            message='my feedback message',
            email='test@email.com'
        )
        self.assertEqual(len(Feedback.objects.all()), 1)

    def test_email_not_required(self):
        Feedback.objects.create(
            subject='Test feedback',
            message='my feedback message',
            email=None
        )
        self.assertEqual(len(Feedback.objects.all()), 1)

    # TODO: Test authenticated user saves to model
    # TODO: Test unauthenticated user
