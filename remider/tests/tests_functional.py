from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import reverse
from django.conf import settings
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time
import os.path


class FunctionalTests(StaticLiveServerTestCase):

    def setUp(self):
        self.MAX_TIME = 10
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def assertUrlNow(self, url, add_secret_key=False, status=200, extras=""):
        if add_secret_key:
            expeted_url = self.live_server_url + reverse(url) + "?key={}".format(settings.SECRET_KEY) + extras
        else:
            expeted_url = self.live_server_url + reverse(url) + extras

        self.assertEqual(self.client.get(self.browser.current_url).status_code, status)
        if status == 200:
            self.assertEqual(self.browser.current_url, expeted_url)

    def wait_and_assertUrlNow(self, url, status=200, extras=''):
        start = time.time()
        while True:
            try:
                self.assertUrlNow(url, add_secret_key=True, status=status, extras=extras)
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

    @override_settings(SECRET_KEY="mycoolsecretkey", LANGUAGE_CODE='en', app_name="benc-test", DEBUG=False)
    def test_logging(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("continue_buton").click()
        self.assertUrlNow(url="get_secret")
        input = self.wait_for_finding(self.browser.find_element_by_id, "id_apisecret")

        input.send_keys("mycoolsecretkey")
        input.send_keys(Keys.ENTER)
        self.wait_and_assertUrlNow(url="menu")

        self.browser.get(self.live_server_url + reverse("get_secret"))
        input = self.wait_for_finding(self.browser.find_element_by_id, "id_apisecret")

        input.send_keys("mynotcoolsecretkey")
        input.send_keys(Keys.ENTER)
        self.wait_and_assertUrlNow(url="menu", status=403)

    @override_settings(SECRET_KEY="mycoolsecretkey", LANGUAGE_CODE='en', app_name="benc-test", DEBUG=False)
    def test_uploading(self):
        self.browser.get(self.live_server_url + reverse("menu") + "?key=mycoolsecretkey")
        self.browser.find_element_by_id("upload_button").click()
        self.wait_and_assertUrlNow("upload")
        input = self.wait_for_finding(self.browser.find_element_by_id, "id_file")
        input.send_keys(os.path.join(settings.BASE_DIR, "remider", "tests", "ATriggerVerify.txt"))
        self.browser.find_element_by_id("upload_button").click()
        self.wait_and_assertUrlNow("menu", extras="&info=1")
