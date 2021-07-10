from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options


class FunctionalTest(StaticLiveServerTestCase):
    host = 'web'

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Remote(
            'http://selenium:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)
        self.browser.get(self.live_server_url)

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
        return self.browser.find_element_by_css_selector('.errorlist')

    def add_dob(self, dob):
        date_input = self.browser.find_element_by_id('id_dob')
        create_button = self.browser.find_element_by_name('create_button')
        date_input.clear()
        date_input.send_keys(dob)
        create_button.click()

    def add_life_event(self, event_name, event_date):
        event_title_input = self.browser.find_element_by_id('id_event_title')
        event_date_input = self.browser.find_element_by_id('id_event_date')
        submit_button = self.browser.find_element_by_name('add_event_btn')
        event_title_input.send_keys(event_name)
        event_date_input.send_keys(event_date)
        submit_button.click()
