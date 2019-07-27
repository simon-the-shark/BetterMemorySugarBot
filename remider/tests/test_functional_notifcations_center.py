from .base import FunctionalTest
from django.shortcuts import reverse
from django.test import override_settings


class NotificationCentrumTest(FunctionalTest):
    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_button(self):
        self.browser.get(self.live_server_url + reverse("menu") + "?key=mycoolsecretkey")
        self.wait_for_finding(lambda: self.browser.find_element_by_css_selector(".btn-primary")).click()
        self.assertUrlNow("notif-center", add_secret_key=True)

    @override_settings(SECRET_KEY="mycoolsecretkey", TRIGGER_IFTTT=False, SEND_SMS=True, TOKEN="")
    def test_posting_forms(self):
        self.browser.get(self.live_server_url + reverse("notif-center") + "?key=mycoolsecretkey")
        ifttt_checkbox = self.wait_for_finding(lambda: self.browser.find_element_by_id("id_ifttt_notifications"))
        sms_checkbox = self.wait_for_finding(lambda: self.browser.find_element_by_id("id_sms_notifications"))
        self.assertFalse(ifttt_checkbox.is_selected())
        self.assertTrue(sms_checkbox.is_selected())
        ifttt_checkbox.click()
        self.browser.find_elements_by_css_selector(".btn-primary")[0].click()
        self.wait_for_finding(lambda: self.check_alert())
        ifttt_checkbox = self.wait_for_finding(lambda: self.browser.find_element_by_id("id_ifttt_notifications"))
        sms_checkbox = self.wait_for_finding(lambda: self.browser.find_element_by_id("id_sms_notifications"))
        self.assertTrue(ifttt_checkbox.is_selected())
        self.assertTrue(sms_checkbox.is_selected())
        sms_checkbox.click()
        self.browser.find_elements_by_css_selector(".btn-primary")[0].click()
        self.check_alert()
        ifttt_checkbox = self.wait_for_finding(lambda: self.browser.find_element_by_id("id_ifttt_notifications"))
        sms_checkbox = self.wait_for_finding(lambda: self.browser.find_element_by_id("id_sms_notifications"))
        self.assertTrue(ifttt_checkbox.is_selected())
        self.assertFalse(sms_checkbox.is_selected())
