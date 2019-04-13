import requests, json, sys, base64
from twilio.rest import Client

from infusionset_reminder.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, from_number, \
    to_numbers, husername, hpassword


# token


def send_message(body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for to_number in to_numbers:
        client.messages.create(body=body,
                               from_=from_number,
                               to=to_number)


def change_config_var(label, new_value):
    print(husername + ":" + "hpassword")
    sys.stdout.flush()
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/vnd.heroku+json; version=3',
               "Authorization": "Basic {}:{}".format(str(base64.b64encode(husername.encode())), hpassword)}
    data = {label: new_value}

    r = requests.patch('https://api.heroku.com/apps/reminder-rekina/config-vars', headers=headers,
                       data=json.dumps(data))
    # if r.status_code == '401':
    #     headers["Authorization"] = "Bearer {}".format(token)
    #     r = requests.patch('https://api.heroku.com/apps/reminder-rekina/config-vars', headers=headers,
    #                        data=json.dumps(data))

    return r.text, r.status_code, headers["Authorization"]
