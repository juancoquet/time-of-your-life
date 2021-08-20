from unittest.mock import patch

from .base import FunctionalTest
from contact.views import FEEDBACK_MESSAGE


@patch('contact.models.Feedback.send_notification')
class FeedbackTest(FunctionalTest):

    def test_feedback_authenticated(self, mock_notification):
        # A logged in user decides to leave feedback.
        self.browser.get(self.live_server_url)
        self.create_user_and_sign_in()

        # They click the feedback link in the navbar.
        self.browser.find_element_by_id('feedback').click()

        # They are taken to the feedback page.
        heading = self.browser.find_element_by_css_selector('.container__text--heading').text
        self.assertEqual(heading, 'Time of Your Life is a work in progress')

        # They see a subject box, a message box and an email box.
        subject = self.browser.find_element_by_id('id_subject')
        message = self.browser.find_element_by_id('id_message')
        email = self.browser.find_element_by_id('id_email')

        # They fill in these fields to leave their feedback.
        subject.send_keys('My feedback')
        message.send_keys('Wow I hated it so much')
        email.send_keys('test@email.com')

        # They click the submit button.
        self.browser.find_element_by_id('id_submit').click()

        # They see a message thanking them for their feedback.
        message = self.browser.find_element_by_css_selector('.banner__message').text
        self.assertEqual(message, FEEDBACK_MESSAGE)

    def test_feedback_not_authenticated(self, mock_notification):
        # A visitor clicks the feedback link in the navbar.
        self.browser.find_element_by_id('feedback').click()

        # They are taken to the feedback page.
        heading = self.browser.find_element_by_css_selector('.container__text--heading').text
        self.assertEqual(heading, 'Time of Your Life is a work in progress')

        # They see a subject box, a message box and an email box.
        subject = self.browser.find_element_by_id('id_subject')
        message = self.browser.find_element_by_id('id_message')
        email = self.browser.find_element_by_id('id_email')

        # They fill in these fields to leave their feedback.
        subject.send_keys('My feedback')
        message.send_keys('Wow I hated it so much')
        email.send_keys('test@email.com')

        # They click the submit button.
        self.browser.find_element_by_id('id_submit').click()

        # They see a message thanking them for their feedback.
        message = self.browser.find_element_by_css_selector('.banner__message').text
        self.assertEqual(message, 'Thanks for your feedback!')
