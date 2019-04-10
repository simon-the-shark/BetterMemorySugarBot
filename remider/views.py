from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.http import FileResponse

import requests as api_rq
from decouple import config
from datetime import datetime, timedelta, timezone

from .sms import send_message
from .forms import GetSecretForm
from infusionset_reminder.settings import SENSOR_ALERT_FREQUENCY, INFUSION_SET_ALERT_FREQUENCY, ATRIGGER_KEY, \
    ATRIGGER_SECRET, SECRET_KEY, app_name
from .models import InfusionChanged, SensorChanged


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
                        try:
                            InfusionChanged.objects.get(id=1).delete()
                        except:
                            pass
                        InfusionChanged.objects.create(id=1, date=date)
                        break
                except:
                    pass

            for set in rjson:
                try:
                    if set['notes'] == 'Sensor changed':
                        sensor_date = set['created_at']
                        try:
                            SensorChanged.objects.get(id=1).delete()
                        except:
                            pass
                        SensorChanged.objects.create(id=1, date=sensor_date)
                        break
                except:
                    pass
        if date is None:
            try:
                date = InfusionChanged.objects.get(id=1).date
            except:
                pass

        if sensor_date is None:
            try:
                sensor_date = SensorChanged.objects.get(id=1).date
            except:
                pass

        idays, ihours, sdays, shours, text = 0, 0, 0, 0, ''

        try:
            """calculate"""
            infusion = timedelta(hours=INFUSION_SET_ALERT_FREQUENCY)
            if type(date) == str:
                infusion_alert_date = datetime.strptime(date[:-6], "%Y-%m-%dT%H:%M:%S") + infusion
            else:
                infusion_alert_date = date + infusion
            infusion_time_remains = infusion_alert_date - datetime.utcnow()
            """notify"""
            idays = infusion_time_remains.days
            ihours = round(infusion_time_remains.seconds / 3600)
            imicroseconds = infusion_time_remains.microseconds
            if idays != 0 or ihours != 0 or imicroseconds != 0:
                text = ".\n.\n Zmień zestaw infuzyjny w {} dni i {} godzin.".format(idays, ihours)

        except:
            text += 'zestaw infuzyjny: nie udało się zczytać danych'

        try:
            """calculate"""
            sensor = timedelta(hours=SENSOR_ALERT_FREQUENCY)
            if type(sensor_date) == str:
                sensor_alert_date = datetime.strptime(sensor_date[:-6], "%Y-%m-%dT%H:%M:%S") + sensor
            else:
                sensor_alert_date = sensor_date + sensor
            sensor_time_remains = sensor_alert_date - datetime.utcnow()
            """notify"""
            sdays = sensor_time_remains.days
            shours = round(sensor_time_remains.seconds / 3600)
            smicroseconds = sensor_time_remains.microseconds
            if sdays != 0 or shours != 0 or smicroseconds != 0:
                text += "\n.\n Zmień sensor CGM w {} dni i {} godzin".format(sdays, shours)
        except:
            text += 'sensor CGM: nie udało się zczytać danych'

        send_message(text)
        create_trigger()

        return render(request, "remider/debug.html",
                      {
                          "idays": idays,
                          "ihours": ihours,
                          "sdays": sdays,
                          "shours": shours,
                      })
    else:
        return HttpResponseForbidden()


def create_trigger():
    fdate = (datetime.utcnow() + timedelta(days=1)).replace(hour=16, minute=0, second=0, microsecond=0).isoformat()

    urll = "https://api.atrigger.com/v1/tasks/create?key={}&secret={}&timeSlice={}&count={}&tag_id=typical&url={}&first={}".format(
        ATRIGGER_KEY, ATRIGGER_SECRET, '1minute', 1,
        'https://{}.herokuapp.com/reminder/?key={}'.format(app_name, SECRET_KEY), fdate)
    api_rq.get(urll)


def file(request):
    file = open("remider/ATriggerVerify.txt", "rb")
    return FileResponse(file)


def auth(request):
    if request.method == "POST":
        form = GetSecretForm(request.POST)
        if form.is_valid():
            return redirect("http://127.0.0.1:8000/menu/?key={}".format(form.cleaned_data['apisecret']))
    else:
        form = GetSecretForm()

    return render(request, "remider/auth.html", context={"form": form})


def menu(request):
    their_key = request.GET.get("key", "")
    if their_key == SECRET_KEY:
        return render(request, "remider/menu.html")
    else:
        return HttpResponseForbidden()


def upload(request):
    return HttpResponseForbidden()
