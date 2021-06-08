from .base import FunctionalTest

from countdown.forms import FUTURE_DOB_ERROR


class NewVisitorTest(FunctionalTest):

    def test_home_page_invites_user_to_enter_date_of_birth(self):
        # A new unauthenticated user visits the site's homepage.
        self.browser.get(self.live_server_url)

        # They notice that the page header and title are "Time of Your Life"
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, "Time of Your Life")
        self.assertEqual(self.browser.title, 'Time of Your Life')

        # They are greeted by a brief explanation of what the web app does.
        description = self.browser.find_element_by_id('site-description').text
        self.assertIn("bird's eye view of your life", description)

        # After reading the explanation, they see a prompt to enter their date of birth.
        date_input = self.browser.find_element_by_id('id_dob')
        create_button = self.browser.find_element_by_name('create_button')

        # They accidentally click the create button without providing a DOB, but the browser intecepts the request
        self.browser.find_element_by_css_selector('#id_dob:invalid')
        create_button.click()

        # They enter a date in the future and they see an error telling them that the date of birth must be in the past
        date_input.send_keys('2999-12-31')
        create_button.click()
        self.assertEqual(self.get_error_element().text, FUTURE_DOB_ERROR)
