from .base import FunctionalTest

from countdown.forms import FUTURE_DOB_ERROR, PAST_DOB_ERROR, EVENT_DATE_ERROR


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
        self.add_dob('2999-12-31')
        self.assertEqual(self.get_error_element().text, FUTURE_DOB_ERROR)

        # They enter a date more than 90 years ago and see an error telling them that the date of birth must be within
        # the past 90 years
        self.add_dob('1901-12-01')
        self.assertEqual(self.get_error_element().text, PAST_DOB_ERROR)

        # They enter a valid DOB, and are shown a grid of boxes representing their life calendar.
        # Getting elements again as page refreshed and old elements are now stale
        self.add_dob('1995-12-01')
        self.assertEqual(
            self.browser.find_element_by_tag_name('h2').text,
            'Your Life Calendar'
        )
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector('.year-row')),
            90
        )

        # Upon closer inspection, they see that some boxes in the grid represent weeks that have already passed,
        # some represent future weeks and one box represents the present week.
        past_weeks = self.browser.find_elements_by_css_selector('.week.past')
        future_weeks = self.browser.find_elements_by_css_selector(
            '.week.future')
        present_week = self.browser.find_elements_by_css_selector(
            '.week.present')
        self.assertGreater(len(past_weeks), 1)
        self.assertGreater(len(future_weeks), 1)
        self.assertEqual(len(present_week), 1)

    def test_grid_page_invites_user_to_add_life_event(self):
        # A new user visits the site and enters a valid DOB
        self.add_dob('1995-12-01')

        # They see a section of the website inviting them to add a life event.
        self.browser.find_element_by_name('add_event')

        # They try to add a date before their date of birth, but they are met with an error.
        self.add_life_event('out of bounds', '1990-01-31')
        self.assertIn(EVENT_DATE_ERROR, self.browser.page_source)

        # They try to add a date outside of their 90-year life window, and once again see the error.
        self.add_life_event('out of bounds', '2085-12-02')
        self.assertIn(EVENT_DATE_ERROR, self.browser.page_source)

        # They insert an event name and a valid date into the form provided.
        self.add_life_event('My event', '2010-03-31')

        # The page refreshes and they see that their event is represented in the calendar as a highlighted box.
        past_weeks = self.browser.find_elements_by_css_selector('.week.past')
        future_weeks = self.browser.find_elements_by_css_selector(
            '.week.future')
        present_week = self.browser.find_elements_by_css_selector(
            '.week.present')
        event_week = self.browser.find_elements_by_css_selector('.week.event')
        all_weeks = self.browser.find_elements_by_css_selector('.week')
        self.assertGreater(len(past_weeks), 1)
        self.assertGreater(len(future_weeks), 1)
        self.assertEqual(len(present_week), 1)
        self.assertEqual(len(event_week), 1)
        self.assertEqual(len(all_weeks), 52*90)

        # After viewing their life calendar for a while, they click the page title and it takes them home.
        header = self.browser.find_element_by_link_text('Time of Your Life')
        header.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/')

    def test_about_page(self):
        # The user wants to find out more about the website, they click the 'about' section.
        self.browser.find_element_by_id('about').click()

        # They are taken to the About page, where they can read more information.
        heading = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(heading, 'About')
