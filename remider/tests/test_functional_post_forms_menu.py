import json
import requests
from django.conf import settings
from django.shortcuts import reverse
from django.test import override_settings
from selenium.webdriver.support.ui import Select

from .base import FunctionalTest


class PostMenuTest(FunctionalTest):
    def setUp(self):
        if settings.TOKEN:
            print(settings.TOKEN)
            print("saving heroku`s config vars")
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
            print("Cleaning up heroku`s config vars...")
            for label in ["ATRIGGER_KEY", "ATRIGGER_SECRET", "INFUSION_SET_ALERT_FREQUENCY", "LANGUAGE_CODE",
                          "NIGHTSCOUT_LINK", "SENSOR_ALERT_FREQUENCY", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"]:
                headers = {'Content-Type': 'application/json',
                           'Accept': 'application/vnd.heroku+json; version=3',
                           "Authorization": "Bearer {}".format(settings.TOKEN)}
                data = {label: self.config_vars_dict.get("label", "")}
                requests.patch('https://api.heroku.com/apps/{}/config-vars'.format(settings.APP_NAME),
                               headers=headers,
                               data=json.dumps(data))
            print("heroku`s config vars restored to previous state")

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
        self.assertPost("id_time", "16:01", clear=True)

    @override_settings(SECRET_KEY="mycoolsecretkey", TOKEN="")
    def test_posting_forms_without_token(self):
        self.test_posting_forms()
