from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

import requests as api_rq
from decouple import config
from datetime import datetime, timedelta, timezone

from .models import InfusionChanged, SensorChanged, Empty
from .whatsapp import send_message
from infusionset_reminder.settings import SENSOR_ALERT_FREQUENCY, INFUSION_SET_ALERT_FREQUENCY, IFTTT_MAKER, SECRET_KEY


def home(request):
    return render(request, "remider/home.html")


def get_from_api(request):
    their_key = request.GET.get("key", "")
    if their_key == SECRET_KEY:
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

            if len(InfusionChanged.objects.all()) == 0 and date != None:
                InfusionChanged.objects.create(date=date, id=1)
            elif date != None and date != InfusionChanged.objects.get(id=1).date:
                InfusionChanged.objects.get(id=1).delete()
                InfusionChanged.objects.create(date=date, id=1)

            for set in rjson:
                try:
                    if set['notes'] == 'Sensor changed':
                        sensor_date = set['created_at']
                        break
                except:
                    pass

            if len(SensorChanged.objects.all()) == 0 and sensor_date != None:
                SensorChanged.objects.create(date=sensor_date, id=1)
            elif sensor_date != None and date != SensorChanged.objects.get(id=1):
                SensorChanged.objects.get(id=1).delete()
                SensorChanged.objects.create(date=sensor_date, id=1)

        return redirect("/calculate/?key={0}".format(SECRET_KEY))
    else:
        return HttpResponseForbidden()


def calculate(request):
    their_key = request.GET.get("key", "")
    if their_key == SECRET_KEY:
        try:
            infusion = timedelta(hours=INFUSION_SET_ALERT_FREQUENCY)
            infusion_alert_date = InfusionChanged.objects.get(id=1).date + infusion
            infusion_time_remains = infusion_alert_date - datetime.now(timezone.utc)
        except:
            infusion_time_remains = Empty()

        try:
            sensor = timedelta(hours=SENSOR_ALERT_FREQUENCY)
            sensor_alert_date = SensorChanged.objects.get(id=1).date + sensor
            sensor_time_remains = sensor_alert_date - datetime.now(timezone.utc)
        except:
            sensor_time_remains = Empty()

        return redirect(
            '/notify?key={6}&idays={0}&ihours={1}&sdays={2}&shours={3}&imicroseconds={4}&smicroseconds={5}'.format(
                infusion_time_remains.days, round(
                    infusion_time_remains.seconds / 3600), sensor_time_remains.days,
                round(sensor_time_remains.seconds / 3600),
                infusion_time_remains.microseconds,
                sensor_time_remains.microseconds,
                SECRET_KEY))
    else:
        return HttpResponseForbidden()


def notify(request):
    idays = request.GET.get("idays", "")
    ihours = request.GET.get("ihours", "")
    sdays = request.GET.get("sdays", "")
    shours = request.GET.get("shours", "")
    imicroseconds = request.GET.get("imicroseconds", "")
    smicroseconds = request.GET.get("smicroseconds", "")
    their_key = request.GET.get("key", "")
    if their_key == SECRET_KEY:
        send_message("---------------------------------------------------------------")
        if idays != 0 or ihours != 0 or imicroseconds != 0:
            send_message("Zmień zestaw infuzyjny w {} dni i {} godzin.".format(idays,ihours))
            # api_rq.post("https://maker.ifttt.com/trigger/reminder/with/key/{0}".format(IFTTT_MAKER),
            #             data={"value1": idays, "value2": ihours, "value3": "infusion set"})
        if sdays != 0 or shours != 0 or smicroseconds != 0:
            send_message("Zmień sensor CGM w {} dni i {} godzin".format(sdays, shours))
            # api_rq.post("https://maker.ifttt.com/trigger/reminder/with/key/{0}".format(IFTTT_MAKER),
            #             data={"value1": sdays, "value2": shours, "value3": "CGM sensor"})

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
