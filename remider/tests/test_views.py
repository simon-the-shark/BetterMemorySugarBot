from django.test import TestCase, override_settings
from django.shortcuts import reverse
from django.conf import settings

from ..forms import GetSecretForm, TriggerTimeForm, ChangeEnvVariableForm, ChooseLanguageForm, \
    ChooseNotificationsWayForm


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


class MenuViewTests(TestCase):
    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_template_loading(self):
        response = self.client.get(reverse("menu") + "?key=mycoolsecretkey")
        self.assertTemplateUsed(response, "remider/menu.html")
        self.assertEqual(response.status_code, 200)

    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_template_contex(self):
        response = self.client.get(reverse("menu") + "?key=mycoolsecretkey")
        self.assertEqual(response.context["SECRET_KEY"], "mycoolsecretkey")
        self.assertEqual(response.context["info"], False)
        self.assertEqual(response.context["info2"], False)
        response = self.client.get(reverse("menu") + "?key=mycoolsecretkey&info=1")
        self.assertEqual(response.context["info"], True)

    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_proper_forms(self):
        response = self.client.get(reverse("menu") + "?key=mycoolsecretkey")
        self.assertIsInstance(response.context["language_form"], ChooseLanguageForm)
        self.assertIsInstance(response.context["time_form"], TriggerTimeForm)
        forms = (
            ("NIGHTSCOUT_LINK", "ns_link_button", settings.NIGTSCOUT_LINK),
            ("INFUSION_SET_ALERT_FREQUENCY", "infusion_freq_button", settings.INFUSION_SET_ALERT_FREQUENCY),
            ("SENSOR_ALERT_FREQUENCY", "sensor_freq_button", settings.SENSOR_ALERT_FREQUENCY),
            ("ATRIGGER_KEY", "atrigger_key_button", settings.ATRIGGER_KEY),
            ("ATRIGGER_SECRET", "atrigger_secret_button", settings.ATRIGGER_SECRET),
            ("TWILIO_ACCOUNT_SID", "twilio_sid_button", settings.TWILIO_ACCOUNT_SID),
            ("TWILIO_AUTH_TOKEN", "twilio_token_button", settings.TWILIO_AUTH_TOKEN),
        )
        for indx, form in enumerate(response.context["forms_list"]):
            self.assertIsInstance(form, ChangeEnvVariableForm)
            self.assertEqual(form.button_name, forms[indx][1])
            self.assertEqual(form.fields['new_value'].label, forms[indx][0])
            self.assertEqual(form.fields['new_value'].initial, forms[indx][2])


class NotificationCenterViewTests(TestCase):
    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_template_loading(self):
        response = self.client.get(reverse("notif-center") + "?key=mycoolsecretkey")
        self.assertTemplateUsed(response, "remider/notifications.html")
        self.assertEqual(response.status_code, 200)

    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_template_context(self):
        response = self.client.get(reverse("notif-center") + "?key=mycoolsecretkey")
        self.assertEqual(response.context["SECRET_KEY"], "mycoolsecretkey")
        self.assertEqual(response.context["trig_info"], True)
        self.assertEqual(response.context["sms_info"], True)

    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_displays_proper_form(self):
        response = self.client.get(reverse("notif-center") + "?key=mycoolsecretkey")
        self.assertIsInstance(response.context['form'], ChooseNotificationsWayForm)
        self.assertContains(response, 'type="checkbox"')
        self.assertContains(response, 'type="submit"')
