from .base import FunctionalTest
from django.shortcuts import reverse
from django.conf import settings
from django.test import override_settings

import os.path


class UploadingTest(FunctionalTest):
    @override_settings(SECRET_KEY="mycoolsecretkey", LANGUAGE_CODE='en', app_name="benc-test", DEBUG=False)
    def test_uploading(self):
        self.browser.get(self.live_server_url + reverse("menu") + "?key=mycoolsecretkey")
        self.browser.find_element_by_id("upload_button").click()
        self.wait_and_assertUrlNow("upload")
        input = self.wait_for_finding(self.browser.find_element_by_id, "id_file")
        input.send_keys(os.path.join(settings.BASE_DIR, "remider", "tests", "ATriggerVerify.txt"))
        self.browser.find_element_by_id("upload_button").click()
        self.wait_and_assertUrlNow("menu", extras="&info=1")
