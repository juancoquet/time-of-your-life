from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class FunctionalTest(StaticLiveServerTestCase):
    host = 'web'

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Remote(
            'http://selenium:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)
        self.browser.get(self.live_server_url)
        self.actions = ActionChains(self.browser)

    def tearDown(self):
        if self._test_has_failed():
            for i, handle in enumerate(self.browser.window_handles):
                self.browser.switch_to.window(handle)
                filepath = self._create_error_capture_filepath(i)
                timestamp = datetime.now()
                self.browser.save_screenshot(
                    f'{filepath}/screenshot-{timestamp}.png')
                self.capture_html(filepath, timestamp)
        self.browser.quit()

    def _test_has_failed(self):
        # returns True if any errors were raised during test run
        return any(error for (method, error) in self._outcome.errors)

    def _create_error_capture_filepath(self, handle_index):
        timestamp = datetime.now()
        classname = self.__class__.__name__
        method = self._testMethodName
        dir_path = f'functional_tests/error_capture/{timestamp}-{classname}.{method}/{handle_index}'
        os.makedirs(dir_path)
        return dir_path

    def capture_html(self, filepath, timestamp):
        filename = f'{filepath}/source-{timestamp}.html'
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.error')

    def add_dob(self, day, month, year):
        day_input = self.browser.find_element_by_id('id_day')
        month_input = self.browser.find_element_by_id('id_month')
        year_input = self.browser.find_element_by_id('id_year')
        day_input.clear()
        month_input.clear()
        year_input.clear()
        day_input.send_keys(day)
        month_input.send_keys(month)
        year_input.send_keys(year)
        create_button = self.browser.find_element_by_name('create_button')
        create_button.click()

    def add_life_event(self, event_name, day, month, year):
        try:
            event_title_input = self.browser.find_element_by_id(
                'id_event_title')
            event_title_input.clear()
            event_title_input.send_keys(event_name)
        except NoSuchElementException:
            event_title_input = self.browser.find_element_by_id(
                'id_event_name')
            event_title_input.clear()
            event_title_input.send_keys(event_name)
        day_input = self.browser.find_element_by_id('id_day')
        month_input = self.browser.find_element_by_id('id_month')
        year_input = self.browser.find_element_by_id('id_year')
        day_input.clear()
        month_input.clear()
        year_input.clear()
        day_input.send_keys(day)
        month_input.send_keys(month)
        year_input.send_keys(year)
        submit_button = self.browser.find_element_by_name('add_event_btn')
        submit_button.click()

    def submit_signup_form(self, username, email, day, month, year, password):
        username_input = self.browser.find_element_by_id('id_username')
        email_input = self.browser.find_element_by_id('id_email')
        day_input = self.browser.find_element_by_id('id_day')
        month_input = self.browser.find_element_by_id('id_month')
        year_input = self.browser.find_element_by_id('id_year')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')
        submit_button = self.browser.find_element_by_id('btn_signup')
        username_input.clear()
        username_input.send_keys(username)
        email_input.clear()
        email_input.send_keys(email)
        day_input.clear()
        month_input.clear()
        year_input.clear()
        day_input.send_keys(day)
        month_input.send_keys(month)
        year_input.send_keys(year)
        password1_input.clear()
        password1_input.send_keys(password)
        password2_input.clear()
        password2_input.send_keys(password)
        submit_button.click()

    def create_user_and_sign_in(self):
        self.browser.find_element_by_id('id_signup').click()
        self.submit_signup_form(
            username='testuser',
            email='test@user.com',
            day='01',
            month='12',
            year='1995',
            password='testpass123'
        )

    def submit_user_update_form(self, email, day, month, year, name):
        email_field = self.browser.find_element_by_id('id_email')
        email_field.clear()
        email_field.send_keys(email)

        day_field = self.browser.find_element_by_id('id_day')
        month_field = self.browser.find_element_by_id('id_month')
        year_field = self.browser.find_element_by_id('id_year')
        day_field.clear()
        month_field.clear()
        year_field.clear()
        day_field.send_keys(day)
        month_field.send_keys(month)
        year_field.send_keys(year)

        name_field = self.browser.find_element_by_id('id_first_name')
        name_field.clear()
        name_field.send_keys(name)

        self.browser.find_element_by_css_selector('.btn.button-submit').click()
