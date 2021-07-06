from .base import FunctionalTest

from countdown.forms import FUTURE_DOB_ERROR, PAST_DOB_ERROR


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

        # They enter a date more than 90 years ago and see an error telling them that the date of birth must be within
        # the past 90 years
        date_input = self.browser.find_element_by_id('id_dob')
        create_button = self.browser.find_element_by_name('create_button')
        date_input.clear()
        date_input.send_keys('1901-12-31')
        create_button.click()
        self.assertEqual(self.get_error_element().text, PAST_DOB_ERROR)

        # They enter a valid DOB, and are shown a grid of boxes representing their life calendar.
        # Getting elements again as page refreshed and old elements are now stale
        date_input = self.browser.find_element_by_id('id_dob')
        create_button = self.browser.find_element_by_name('create_button')
        date_input.clear()
        date_input.send_keys('1995-12-01')
        create_button.click()
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
        date_input = self.browser.find_element_by_id('id_dob')
        create_button = self.browser.find_element_by_name('create_button')
        date_input.send_keys('1995-12-01')
        create_button.click()

        # They see a section of the website inviting them to add a life event.
        add_event = self.browser.find_element_by_name('add_event')
        # They insert an event name and a date into the form provided.
        event_title_input = self.browser.find_element_by_id('id_event_title')
        event_date_input = self.browser.find_element_by_id('id_event_date')
        submit_button = self.browser.find_element_by_name('add_event_btn')
        event_title_input.send_keys('My event')
        event_date_input.send_keys('2010-03-31')
        submit_button.click()

        # The page refreshes and they see that their event is represented in the calendar as a highlighted box.
        past_weeks = self.browser.find_elements_by_css_selector('.week.past')
        future_weeks = self.browser.find_elements_by_css_selector(
            '.week.future')
        present_week = self.browser.find_elements_by_css_selector(
            '.week.present')
        event_week = self.browser.find_elements_by_css_selector('.week.event')
        self.assertGreater(len(past_weeks), 1)
        self.assertGreater(len(future_weeks), 1)
        self.assertEqual(len(present_week), 1)
        self.assertEqual(len(event_week), 1)

        # TODO: test cannot add event date outside life calendar
        # TODO: test can add multiple events
        # TODO: test tooltip appears on event hover

        # After viewing their life calendar for a while, they click the page title and it takes them home.
        header = self.browser.find_element_by_link_text('Time of Your Life')
        header.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/')
