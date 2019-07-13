from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import reverse
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time


class FunctionalTests(StaticLiveServerTestCase):

    def setUp(self):
        self.MAX_TIME = 10
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def assertUrlNow(self, url, add_secret_key=False, status=200):
        if add_secret_key:
            expeted_url = self.live_server_url + reverse(url) + "?key={}".format(settings.SECRET_KEY)
        else:
            expeted_url = self.live_server_url + reverse(url)

        self.assertEqual(self.browser.current_url, expeted_url)
        self.assertEqual(self.client.get(self.browser.current_url).status_code, status)

    def wait_and_assertUrlNow(self, url, status=200):
        start = time.time()
        while True:
            try:
                self.assertUrlNow(url, add_secret_key=True, status=status)
                return
            except AssertionError as e:
                if time.time() - start > self.MAX_TIME:
                    raise e
                time.sleep(0.5)

    def wait_for_finding(self, find_expression, *args):
        start = time.time()
        while True:
            try:
                return find_expression(*args)
            except WebDriverException as e:
                if time.time() - start > self.MAX_TIME:
                    raise e
                time.sleep(0.5)

    def test_logging(self):
        self.browser.get(self.live_server_url)
        self.assertIn(self.browser.title, "BetterMemorySugarBot")
        self.browser.find_element_by_id("continue_buton").click()
        self.assertUrlNow(url="get_secret")
        input = self.wait_for_finding(self.browser.find_element_by_id, "id_apisecret")

        with self.settings(SECRET_KEY="mycoolsecretkey"):
            input.send_keys("mycoolsecretkey")
            input.send_keys(Keys.ENTER)
            self.wait_and_assertUrlNow(url="menu")

        self.browser.get(self.live_server_url + reverse("get_secret"))
        input = self.wait_for_finding(self.browser.find_element_by_id, "id_apisecret")
        with self.settings(SECRET_KEY="my cool secret key"):
            input.send_keys("my not cool secret key")
            input.send_keys(Keys.ENTER)
            self.wait_and_assertUrlNow(url="menu", status=403)

