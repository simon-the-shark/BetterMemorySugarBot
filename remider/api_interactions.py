import json
import sys
from datetime import datetime, timedelta

import requests.exceptions
from django.conf import settings
from django.utils.translation import ugettext as _
from twilio.rest import Client

from .data_processing import not_today, update_last_triggerset, get_trigger_model


def notify(sms_text):
    """
    sends notifications via chosen ways
    :param sms_text: text of notification
    """
    if settings.SEND_SMS:
        send_message(sms_text)
    if settings.TRIGGER_IFTTT:
        send_webhook_IFTTT(val1=sms_text[1:])


def send_webhook_IFTTT(val1="", val2="", val3=""):
    """ sends IFTTT webhook to all of ifttt makers from ifttt_makers list """
    for IFTTT_MAKER in settings.IFTTT_MAKERS:
        r = requests.post("https://maker.ifttt.com/trigger/sugarbot-notification/with/key/{0}".format(IFTTT_MAKER),
                          data={"value1": val1, "value2": val2, "value3": val3})
        if r.status_code != 200:
            print(_("error: unsuccessful IFTTT notification to {}").format(str(IFTTT_MAKER)))
            sys.stdout.flush()


def send_message(body):
    """ sends sms via Twilio gateway """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    except:
        print("unsuccessfull twilio client creation.")
        sys.stdout.flush()

    for to_number in settings.TO_NUMBERS:
        try:
            client.messages.create(body=body, from_=settings.FROM_NUMBER, to=to_number)
        except:
            print(_("error: unsuccessful notification to {}").format(str(to_number)))
            sys.stdout.flush()


def change_config_var(label, new_value):
    """ changes config variables on heroku.com"""
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/vnd.heroku+json; version=3',
               "Authorization": "Bearer {}".format(settings.TOKEN)}
    data = {label: new_value}

    r = requests.patch('https://api.heroku.com/apps/{}/config-vars'.format(settings.APP_NAME), headers=headers,
                       data=json.dumps(data))

    if r.status_code == 200:
        return True
    else:
        print(r.text)
        sys.stdout.flush()
        return False


def create_trigger(tag="typical"):
    """ creates trigger on atrigger.com """
    if not_today():
        time_model = get_trigger_model()
        notif_date = (datetime.utcnow() + timedelta(days=1)).replace(hour=time_model.time.hour,
                                                                     minute=time_model.time.minute,
                                                                     second=time_model.time.second,
                                                                     microsecond=0).isoformat()

        url = "https://api.atrigger.com/v1/tasks/create?key={}&secret={}&timeSlice={}&count={}&tag_id={}&url={}&first={}".format(
            settings.ATRIGGER_KEY, settings.ATRIGGER_SECRET, '1minute', 1, tag,
            'https://{}.herokuapp.com/reminder/?key={}'.format(settings.APP_NAME, settings.SECRET_KEY), notif_date)
        r = requests.get(url)

        if r.status_code == 200:
            update_last_triggerset()
            return True
        else:
            print(_(
                "unsuccessful trigger on atrigger.com creating \n perhaps wrong API key or secret ?? or an app_name ??"))
            sys.stdout.flush()
            return False
