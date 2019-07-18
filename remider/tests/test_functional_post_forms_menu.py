from .base import FunctionalTest
from django.shortcuts import reverse
from django.test import override_settings
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class PostMenuTest(FunctionalTest):
    def check_alert(self):
        alert = self.wait_for_finding(lambda: self.browser.find_element_by_css_selector(".alert"))
        if self.live_server_url.startswith("http://localhost"):
            self.assertIn("alert-danger", alert.get_attribute("class"))
        else:
            self.assertIn("alert-success", alert.get_attribute("class"))

    def assertPost(self, id, new_value, indx=0, backspaces=0):
        input = self.wait_for_finding(lambda: self.browser.find_elements_by_id(id))[indx]
        for i in range(backspaces):
            input.send_keys(Keys.BACK_SPACE)
        input.send_keys(new_value)
        input.send_keys(Keys.ENTER)
        self.check_alert()

    def assertChangeEnvVarPost(self, indx, new_value, ):
        self.assertPost("id_new_value", new_value, indx)

    def assertDropdownSelectPost(self, id, new_value, indx=0):
        select_input = Select(self.wait_for_finding(lambda: self.browser.find_elements_by_id(id))[indx])
        select_input.select_by_value(new_value)
        self.browser.find_element_by_name("language_button").click()
        self.check_alert()

    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_posting_forms(self):
        self.browser.get(self.live_server_url + reverse("menu") + "?key=mycoolsecretkey")
        self.assertDropdownSelectPost("id_language", "en")
        self.assertChangeEnvVarPost(0, "https://benc.com")
        self.assertChangeEnvVarPost(1, 73)
        self.assertChangeEnvVarPost(2, 144)
        self.assertChangeEnvVarPost(3, "akey")
        self.assertChangeEnvVarPost(4, "asecret")
        self.assertChangeEnvVarPost(5, "tsid")
        self.assertChangeEnvVarPost(6, "tsecret")
        self.assertPost("id_time", "16:01", backspaces=5)
