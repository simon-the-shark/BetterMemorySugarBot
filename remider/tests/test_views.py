from django.test import TestCase, override_settings
from django.shortcuts import reverse

from ..forms import GetSecretForm


class HomeViewTests(TestCase):
    def test_template_loading(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "remider/home.html")
        self.assertEqual(response.status_code, 200)


class AuthViewTests(TestCase):
    def test_template_loading(self):
        response = self.client.get(reverse("get_secret"))
        self.assertTemplateUsed(response, "remider/auth.html")
        self.assertEqual(response.status_code, 200)

    def test_displays_proper_form(self):
        response = self.client.get(reverse("get_secret"))
        self.assertIsInstance(response.context['form'], GetSecretForm)
        self.assertContains(response, 'type="password"')
        self.assertContains(response, 'type="submit"')