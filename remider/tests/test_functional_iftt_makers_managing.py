from .base import HerokuFunctionalTest, check_internet_connection
from django.shortcuts import reverse
from django.test import override_settings
from selenium.webdriver.common.keys import Keys
import os
from unittest import skipIf
import time
from django.conf import settings


class IFTTTTests(HerokuFunctionalTest):

    def get_inputs_list(self):
        return self.wait_for_finding(lambda: self.browser.find_elements_by_id("id_new_value"))

    def get_input(self, id):
        return self.get_inputs_list()[id]

    def assertInputsLen(self, length):
        start = time.time()
        while True:
            try:
                self.assertEqual(len(self.get_inputs_list()), length)
                return
            except AssertionError as e:
                if time.time() - start > self.MAX_TIME:
                    raise e
                time.sleep(0.5)

    def postInput(self, indx, new_value):
        input = self.get_input(indx)
        input.send_keys(new_value)
        self.wait_for_finding(lambda: self.browser.find_elements_by_css_selector(".btn-primary")[indx].click())

    def changeInput(self, indx, new_value):
        input = self.get_input(indx)
        input.clear()
        input.send_keys(new_value)
        self.wait_for_finding(lambda: self.browser.find_elements_by_css_selector(".btn-primary")[indx].click())

    def fix_local_variables(self, new_value, chanaged=False, indx=None):
        if self.live_server_url.startswith("http://localhost"):
            if not chanaged:
                settings.IFTTT_MAKERS.append(new_value)
            else:
                settings.IFTTT_MAKERS[indx] = new_value

    def delete(self, expected):
        self.wait_for_finding(lambda: self.browser.find_element_by_css_selector(".btn-danger")).click()
        self.wait_and_assertUrlNow("manage_ifttt_makers",
                                   extras="&delinfo=1&delid={}".format(len(settings.IFTTT_MAKERS)))
        alert = self.wait_for_finding(lambda: self.browser.find_element_by_css_selector(".alert"))
        self.assertIn("alert-danger", alert.get_attribute("class"))
        self.assertEqual(settings.IFTTT_MAKERS.pop(-1), expected)

    @override_settings(SECRET_KEY="mycoolsecretkey", LANGUAGE_CODE='en', app_name="benc-test", DEBUG=True,
                       IFTTT_MAKERS=[], )
    def test_multiple_forms_behavior(self):
        self.browser.get(self.live_server_url + reverse("manage_ifttt_makers") + "?key=mycoolsecretkey")
        self.postInput(0, "maker one")
        self.wait_and_assertUrlNow("manage_ifttt_makers")
        self.check_alert()
        self.assertInputsLen(2)
        self.fix_local_variables("maker one")

        self.postInput(1, "maker two")
        self.wait_and_assertUrlNow("manage_ifttt_makers")
        self.check_alert()
        self.assertInputsLen(3)
        self.fix_local_variables("maker two")

        self.postInput(2, "maker three")
        self.wait_and_assertUrlNow("manage_ifttt_makers")
        self.check_alert()
        self.assertInputsLen(4)
        self.fix_local_variables("maker three")

        self.changeInput(0, "changed maker one")
        self.wait_and_assertUrlNow("manage_ifttt_makers")
        self.check_alert()
        self.assertInputsLen(4)
        self.fix_local_variables("changed maker one", chanaged=True, indx=0)

        self.delete("maker three")
        self.assertInputsLen(3)

        self.delete("maker two")
        self.assertInputsLen(2)

        self.wait_and_assertUrlNow("manage_ifttt_makers", extras="&delinfo=1&delid=2")
        self.postInput(1, "new maker two")
        self.wait_and_assertUrlNow("manage_ifttt_makers", extras="&delinfo=1&delid=2")
        self.wait_for_finding(lambda: self.check_alert())
        self.assertInputsLen(3)
        self.fix_local_variables("new maker two")

        self.changeInput(1, "cool maker")
        self.wait_and_assertUrlNow("manage_ifttt_makers", extras="&delinfo=1&delid=2")
        self.check_alert()
        self.assertInputsLen(3)
        self.fix_local_variables("cool maker", chanaged=True, indx=1)
