from .base import FunctionalTest
from django.shortcuts import reverse
from django.conf import settings
from django.test import override_settings

import os.path


class UploadingTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        try:
            with open(os.path.join(settings.STATIC_ROOT, "uplouded", "ATriggerVerify.txt")) as file:
                self.file = file.read()
        except FileNotFoundError:
            self.file = False

    def tearDown(self):
        super().tearDown()
        if self.file:
            with open(os.path.join(settings.STATIC_ROOT, "uplouded", "ATriggerVerify.txt"), "w+") as file:
                file.write(str(self.file))

    @override_settings(DEBUG=True, SECRET_KEY="mycoolsecretkey")
    def test_templates(self):
        response = self.client.get(reverse("upload") + "?key=mycoolsecretkey")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "remider/upload.html")

    def uplouding_test(self, file_path):
        self.browser.get(self.live_server_url + reverse("menu") + "?key=mycoolsecretkey")
        self.browser.find_element_by_id("upload_button").click()
        self.wait_and_assertUrlNow("upload")
        input = self.wait_for_finding(lambda: self.browser.find_element_by_id("id_file"))
        input.send_keys(file_path)
        self.browser.find_element_by_id("upload_button").click()
        self.wait_and_assertUrlNow("menu", extras="&info=1")

        with open(file_path, "rb") as file:
            file = file.read()
            response = self.client.get(reverse("atriggerfile"))
            self.assertContains(response, file)

    @override_settings(SECRET_KEY="mycoolsecretkey", LANGUAGE_CODE='en', app_name="benc-test", DEBUG=True)
    def test_uploading(self):
        self.uplouding_test(file_path=os.path.join(settings.BASE_DIR, "remider", "tests", "ATriggerVerify.txt"))
        self.uplouding_test(file_path=os.path.join(settings.BASE_DIR, "remider", "tests", "ATriggerVerify2.txt"))
