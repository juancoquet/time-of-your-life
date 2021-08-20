from .base import FunctionalTest

from countdown.forms import FUTURE_DOB_ERROR, PAST_DOB_ERROR, EVENT_DATE_ERROR


class NewVisitorTest(FunctionalTest):

    def test_home_page_invites_user_to_enter_date_of_birth(self):
        # A new unauthenticated user visits the site's homepage.
        self.browser.get(self.live_server_url)

        # They notice that the page header and title are "Time of Your Life"
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, "TIME of YOUR LIFE")
        self.assertEqual(self.browser.title, 'Time of Your Life')

        # They are greeted by a brief explanation of what the web app does.
        description = self.browser.find_element_by_id('site-description').text
        self.assertIn("View the current week of your life", description)

        # After reading the explanation, they see a prompt to enter their date of birth.
        self.browser.find_element_by_id('id_day')
        self.browser.find_element_by_id('id_month')
        self.browser.find_element_by_id('id_year')
        create_button = self.browser.find_element_by_name('create_button')

        # They accidentally click the create button without providing a DOB, but the browser intecepts the request
        self.browser.find_element_by_css_selector('#id_year:invalid')
        create_button.click()

        # They enter a date in the future and they see an error telling them that the date of birth must be in the past
        self.add_dob(day='31', month='12', year='2999')
        self.assertEqual(self.get_error_element().text, FUTURE_DOB_ERROR)

        # They enter a date more than 90 years ago and see an error telling them that the date of birth must be within
        # the past 90 years
        self.add_dob(day='01', month='12', year='1901')
        self.assertEqual(self.get_error_element().text, PAST_DOB_ERROR)

        # They enter a valid DOB, and are shown a grid of boxes representing their life calendar.
        # Getting elements again as page refreshed and old elements are now stale
        self.add_dob(day='01', month='12', year='1995')
        self.assertEqual(
            self.browser.find_element_by_css_selector('.container__heading--left').text,
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
        self.add_dob(day='01', month='12', year='1995')

        # They see a section of the website inviting them to add a life event.
        self.browser.find_element_by_name('add_event')

        # They try to add a date before their date of birth, but they are met with an error.
        self.add_life_event(
            event_name='out of bounds',
            day='31',
            month='01',
            year='1990',
        )
        self.assertIn(EVENT_DATE_ERROR, self.browser.page_source)

        # They try to add a date outside of their 90-year life window, and once again see the error.
        self.add_life_event(
            event_name='out of bounds',
            day='02',
            month='12',
            year='2085',
        )
        self.assertIn(EVENT_DATE_ERROR, self.browser.page_source)

        # They insert an event name and a valid date into the form provided.
        self.add_life_event(
            event_name='my event',
            day='31',
            month='03',
            year='2010',
        )

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
        logo = self.browser.find_element_by_id('home')
        logo.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/')

    def test_about_page(self):
        # The user wants to find out more about the website, they click the 'about' section.
        self.browser.find_element_by_id('about').click()

        # They are taken to the About page, where they can read more information.
        heading = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Counting the remaining weeks of your life', heading)
