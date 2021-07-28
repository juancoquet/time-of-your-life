from .base import FunctionalTest


class FeedbackTest(FunctionalTest):

    def test_feedback_authenticated(self):
        # A logged in user decides to leave feedback.
        self.create_user_and_sign_in()

        # They click the feedback link in the navbar.
        self.browser.find_element_by_id('feedback').click()

        # They are taken to the feedback page.
        heading = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual(heading, 'Leave feedback')

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
        message = self.browser.find_element_by_css_selector('.message').text
        self.assertEqual(message, 'Thanks for your feedback!')

    def test_feedback_not_authenticated(self):
        # A visitor clicks the feedback link in the navbar.
        self.browser.find_element_by_id('feedback').click()

        # They are taken to the feedback page.
        heading = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual(heading, 'Leave feedback')

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
        message = self.browser.find_element_by_css_selector('.message').text
        self.assertEqual(message, 'Thanks for your feedback!')
