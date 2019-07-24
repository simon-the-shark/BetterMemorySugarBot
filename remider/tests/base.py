from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import reverse
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import requests

import time
import json


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.MAX_TIME = 10
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def assertUrlNow(self, url, add_secret_key=False, status=200, extras=""):
        if url.startswith("https://"):
            expeted_url = url
        elif add_secret_key:
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

    def wait_for_finding(self, find_expression):
        start = time.time()
        while True:
            try:
                return find_expression()
            except (WebDriverException, AssertionError) as e:
                if time.time() - start > self.MAX_TIME:
                    raise e
                time.sleep(0.5)

    def assertPost(self, id, new_value, indx=0, clear=False):
        input = self.wait_for_finding(lambda: self.browser.find_elements_by_id(id))[indx]
        if clear:
            input.clear()
        input.send_keys(new_value)
        input.send_keys(Keys.ENTER)
        self.check_alert()

    def check_alert(self):
        alert = self.wait_for_finding(lambda: self.browser.find_element_by_css_selector(".alert"))
        if not settings.TOKEN:
            self.assertIn("alert-danger", alert.get_attribute("class"))
        else:
            self.assertIn("alert-success", alert.get_attribute("class"))


class HerokuFunctionalTest(FunctionalTest):
    def setUp(self):
        self.MAX_TIMES = 5
        if settings.TOKEN:
            print("saving heroku`s config vars...")
            vars = requests.get('https://api.heroku.com/apps/{}/config-vars'.format(settings.APP_NAME), headers={
                'Accept': 'application/vnd.heroku+json; version=3',
                "Authorization": "Bearer {}".format(settings.TOKEN)
            })
            self.config_vars_dict = json.loads(vars.text)
            print("heroku`s config vars saved")

        super().setUp()

    def tearDown(self):
        super().tearDown()

        if settings.TOKEN:
            i = 0
            while True:
                i += 1
                try:
                    print("Cleaning up heroku`s config vars...")
                    data = {}
                    for label, val in self.config_vars_dict.items():
                        data[label] = val

                    headers = {'Content-Type': 'application/json',
                               'Accept': 'application/vnd.heroku+json; version=3',
                               "Authorization": "Bearer {}".format(settings.TOKEN)}
                    requests.patch('https://api.heroku.com/apps/{}/config-vars'.format(settings.APP_NAME),
                                   headers=headers,
                                   data=json.dumps(data))
                    print("heroku`s config vars restored to previous state")
                    return
                except (requests.exceptions.ConnectionError) as e:
                    print("!!an error occured!!!")
                    if i < self.MAX_TIMES:
                        print("trying again... It`s {} attempt".format(str(i)))
                    else:
                        raise e


def check_internet_connection():
    try:
        requests.get("https://www.google.com/")
        return True
    except requests.ConnectionError:
        return False
