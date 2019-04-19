import requests, json
from datetime import datetime, timedelta

from twilio.rest import Client

from infusionset_reminder.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, from_number, \
    to_numbers, token, ATRIGGER_KEY, ATRIGGER_SECRET, app_name, SECRET_KEY


def send_message(body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for to_number in to_numbers:
        try:
            client.messages.create(body=body, from_=from_number, to=to_number)
        except:
            pass


def change_config_var(label, new_value):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/vnd.heroku+json; version=3',
               "Authorization": "Bearer {}".format(token)}
    data = {label: new_value}

    requests.patch('https://api.heroku.com/apps/reminder-rekina/config-vars', headers=headers,
                   data=json.dumps(data))


def create_trigger():
    notif_date = (datetime.utcnow() + timedelta(days=1)).replace(hour=16, minute=0, second=0, microsecond=0).isoformat()

    url = "https://api.atrigger.com/v1/tasks/create?key={}&secret={}&timeSlice={}&count={}&tag_id=typical&url={}&first={}".format(
        ATRIGGER_KEY, ATRIGGER_SECRET, '1minute', 1,
        'https://{}.herokuapp.com/reminder/?key={}'.format(app_name, SECRET_KEY), notif_date)
    requests.get(url)
