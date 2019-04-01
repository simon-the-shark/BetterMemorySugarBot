from twilio.rest import Client
from infusionset_reminder.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, from_whatsapp_number, \
    to_whatsapp_numbers


def send_message(body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for to_whatsapp_number in to_whatsapp_numbers:
        client.messages.create(body=body,
                               from_=from_whatsapp_number,
                               to=to_whatsapp_number)
