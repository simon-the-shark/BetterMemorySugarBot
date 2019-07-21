from .base import FunctionalTest, check_internet_connection
from django.shortcuts import reverse
from django.test import override_settings
from unittest import skipIf


class CSSTests(FunctionalTest):

    @skipIf(not check_internet_connection(), "no internet connection")
    def test_home_view(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        hello_world = self.browser.find_element_by_css_selector(".display-4")
        self.assertAlmostEqual(
            hello_world.location['x'],
            73,
            delta=20
        )

    @skipIf(not check_internet_connection(), "no internet connection")
    def test_auth_view(self):
        self.browser.get(self.live_server_url + reverse("get_secret"))
        self.browser.set_window_size(1024, 768)
        form = self.browser.find_element_by_css_selector("form")
        self.assertAlmostEqual(
            form.location['x'],
            41,
            delta=20
        )

    @skipIf(not check_internet_connection(), "no internet connection")
    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_menu_view(self):
        self.browser.get(self.live_server_url + reverse("menu")+"?key=mycoolsecretkey")
        self.browser.set_window_size(1024, 768)
        settings = self.browser.find_element_by_css_selector(".display-4")
        self.assertAlmostEqual(
            settings.location['x'],
            32,
            delta=20
        )

    @skipIf(not check_internet_connection(), "no internet connection")
    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_notif_center_view(self):
        self.browser.get(self.live_server_url + reverse("notif-center") + "?key=mycoolsecretkey")
        self.browser.set_window_size(1024, 768)
        settings = self.browser.find_element_by_css_selector(".btn-info")
        self.assertAlmostEqual(
            settings.location['x'],
            43,
            delta=20
        )
