import sys
from datetime import datetime, timedelta, timezone

from infusionset_reminder.settings import INFUSION_SET_ALERT_FREQUENCY, SENSOR_ALERT_FREQUENCY
from .languages import *
from .models import InfusionChanged, SensorChanged


def process_nightscouts_api_response(response):
    """
    process nightscout`s response and return date and time of last change of infusion set and CGM sensor
    saves it in database
    if data not in response, get from database (if present)

    :param response: response from nightscout`s API
    :return: last change date and time
    """
    if response.status_code == 200:
        inf_date = None
        sensor_date = None

        response_text = response.json()

        for set in response_text:
            try:
                if inf_date is None and set['notes'] == "Reservoir changed":
                    inf_date = set["created_at"]
                    InfusionChanged.objects.update_or_create(id=1, defaults={"date": inf_date, })
                elif sensor_date is None and set['notes'] == "Sensor changed":
                    sensor_date = set['created_at']
                    SensorChanged.objects.update_or_create(id=1, defaults={"date": sensor_date, })
            except KeyError:
                pass

        try:
            inf_date = InfusionChanged.objects.get(id=1).date
        except InfusionChanged.DoesNotExist:
            print("warning: infusion set change has never been cached")
            sys.stdout.flush()

        try:
            sensor_date = SensorChanged.objects.get(id=1).date
        except SensorChanged.DoesNotExist:
            print("warning: CGM sensor change has never been cached")
            sys.stdout.flush()

        return inf_date, sensor_date


def calculate_infusion(date):
    """
    calculates next change of infusion set
    :param date: datetime of previous change of infusion set
    :return: time remains to next change
    """
    infusion = timedelta(hours=INFUSION_SET_ALERT_FREQUENCY)
    infusion_alert_date = date + infusion
    infusion_time_remains = infusion_alert_date - datetime.now(timezone.utc)

    return infusion_time_remains


def calculate_sensor(date):
    """
    calculates next change of CGM sensor
    :param date:  datetime of previous change of CGM sensor
    :return: time remains to next change
    """
    sensor = timedelta(hours=SENSOR_ALERT_FREQUENCY)
    sensor_alert_date = date + sensor
    sensor_time_remains = sensor_alert_date - datetime.now(timezone.utc)

    return sensor_time_remains


def get_sms_txt_infusion_set(time_remains):
    """
     add info about next change of infusion set to sms`s text
    :param time_remains: timedelta to next change
    :return: part of text for sms notification
    """
    days = time_remains.days
    hours = round(time_remains.seconds / 3600)
    text = languages_infusion_successful.format(days, hours)

    return text


def get_sms_txt_sensor(time_remains):
    """
    add info about next change of CGM sensor to sms`s text
    :param time_remains: timedelta to next change
    :return: part of text for sms notification
    """
    days = time_remains.days
    hours = round(time_remains.seconds / 3600)
    text = languages_sensor_successful.format(days, hours)

    return text
