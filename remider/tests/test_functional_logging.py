from .base import FunctionalTest
from django.shortcuts import reverse
from django.test import override_settings
from selenium.webdriver.common.keys import Keys


class LoggingTest(FunctionalTest):
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
