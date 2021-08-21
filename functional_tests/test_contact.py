from unittest.mock import patch

from .base import FunctionalTest


@patch('contact.models.Contact.send_notification')
class ContactTest(FunctionalTest):

    def test_contact_authenticated(self, mock_notification):
        # A logged in user decides to get in touch.
        self.browser.get(self.live_server_url)
        self.create_user_and_sign_in()

        # They click the contact link in the navbar.
        self.browser.find_element_by_id('contact').click()

        # They are taken to the contact page.
        heading = self.browser.find_element_by_css_selector('.container__text--heading').text
        self.assertEqual(heading, "Don't be shy...")

        # They see a subject box, a message box and an email box
        subject = self.browser.find_element_by_id('id_subject')
        message = self.browser.find_element_by_id('id_message')
        email = self.browser.find_element_by_id('id_email')

        # They fill in these fields to leave their message.
        subject.send_keys('Contact me')
        message.send_keys('This is my contact message')
        email.send_keys('test@email.com')

        # They click the submit button.
        self.browser.find_element_by_id('id_submit').click()

        # They see a message letting them know that their message was sent.
        message = self.browser.find_element_by_css_selector('.banner__message').text
        self.assertEqual(message, "Message sent")


@patch('contact.models.Contact.send_notification')
class UnauthContactTest(FunctionalTest):

    def test_contact_unauthenticated(self, mock_notification):
        # A new visitor clicks the contact link in the navbar.
        self.browser.find_element_by_id('contact').click()

        # They are taken to the contact page.
        heading = self.browser.find_element_by_css_selector('.container__text--heading').text
        self.assertEqual(heading, "Don't be shy...")

        # They see a subject box, a message box and an email box
        subject = self.browser.find_element_by_id('id_subject')
        message = self.browser.find_element_by_id('id_message')
        email = self.browser.find_element_by_id('id_email')

        # They fill in these fields to leave their message.
        subject.send_keys('Contact me')
        message.send_keys('This is my contact message')
        email.send_keys('test@email.com')

        # They click the submit button.
        self.browser.find_element_by_id('id_submit').click()

        # They see a message letting them know that their message was sent.
        message = self.browser.find_element_by_css_selector('.banner__message').text
        self.assertEqual(message, "Message sent")
