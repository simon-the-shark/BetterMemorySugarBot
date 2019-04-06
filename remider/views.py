from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.http import FileResponse

import requests as api_rq
from decouple import config
from datetime import datetime, timedelta

from .sms import send_message
from infusionset_reminder.settings import SENSOR_ALERT_FREQUENCY, INFUSION_SET_ALERT_FREQUENCY, ATRIGGER_KEY, \
    ATRIGGER_SECRET, SECRET_KEY


def home(request):
    return render(request, "remider/home.html")


def reminder_view(request):
    their_key = request.GET.get("key", "")
    if their_key == SECRET_KEY:
        """get_from_api"""
        date = None
        sensor_date = None
        r = api_rq.get(config("NIGHTSCOUT_LINK") + "/api/v1/treatments")
        rjson = r.json()
        if r.status_code == 200:
            for set in rjson:
                try:
                    if set['notes'] == 'Reservoir changed':
                        date = set['created_at']
                        break
                except:
                    pass

            for set in rjson:
                try:
                    if set['notes'] == 'Sensor changed':
                        sensor_date = set['created_at']
                        break
                except:
                    pass
        """calculate"""
        infusion = timedelta(hours=INFUSION_SET_ALERT_FREQUENCY)
        infusion_alert_date = datetime.strptime(date[:-6], "%Y-%m-%dT%H:%M:%S") + infusion
        infusion_time_remains = infusion_alert_date - datetime.now()

        sensor = timedelta(hours=SENSOR_ALERT_FREQUENCY)
        sensor_alert_date = datetime.strptime(sensor_date[:-6], "%Y-%m-%dT%H:%M:%S") + sensor
        sensor_time_remains = sensor_alert_date - datetime.now()

        """notify"""
        idays = infusion_time_remains.days
        ihours = round(infusion_time_remains.seconds / 3600)
        sdays = sensor_time_remains.days
        shours = round(sensor_time_remains.seconds / 3600)
        imicroseconds = infusion_time_remains.microseconds
        smicroseconds = sensor_time_remains.microseconds
        text = ''
        if idays != 0 or ihours != 0 or imicroseconds != 0:
            text = ".\n.\n Zmień zestaw infuzyjny w {} dni i {} godzin.".format(idays, ihours)
        if sdays != 0 or shours != 0 or smicroseconds != 0:
            text += "\n.\n Zmień sensor CGM w {} dni i {} godzin".format(sdays, shours)

        send_message(text)
        create_trigger()

        return render(request, "remider/debug.html",
                      {
                          "value3": "infusion set",
                          "value32": "CGM sensor",
                          "value1": idays,
                          "value12": sdays,
                          "value2": ihours,
                          "value22": shours,
                      })
    else:
        return HttpResponseForbidden()


def create_trigger():
    fdate = (datetime.utcnow() + timedelta(days=1)).replace(hour=16,minute=0,second=0,microsecond=0).isoformat()

    urll = "https://api.atrigger.com/v1/tasks/create?key={}&secret={}&timeSlice={}&count={}&tag_id=typical&url={}&first={}".format(
        ATRIGGER_KEY, ATRIGGER_SECRET, '1minute', 1,
        'https://reminder-rekina.herokuapp.com/reminder/?key={}'.format(SECRET_KEY), fdate)
    api_rq.get(urll)


def file(request):
    file = open("remider/ATriggerVerify.txt", "rb")
    return FileResponse(file)
