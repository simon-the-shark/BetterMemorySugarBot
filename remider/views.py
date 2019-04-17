from django.shortcuts import render, redirect
from django.http import FileResponse
from django.views.generic import TemplateView

import requests as api_rq
from datetime import datetime, timedelta, timezone

from .api_interactions import send_message
from .forms import GetSecretForm, FileUploudForm
from infusionset_reminder.settings import SENSOR_ALERT_FREQUENCY, INFUSION_SET_ALERT_FREQUENCY, ATRIGGER_KEY, \
    ATRIGGER_SECRET, SECRET_KEY, app_name, nightscout_link, TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_SID, from_number, \
    to_numbers
from .models import InfusionChanged, SensorChanged
from .decorators import secret_key_required
from .forms_management import create_changeenvvarform, save_changeenvvarform
from .forms import ChangeEnvVariableForm
from .api_interactions import change_config_var


@secret_key_required
def reminder_view(request):
    """get_from_api"""
    date = None
    sensor_date = None
    r = api_rq.get(nightscout_link + "/api/v1/treatments")
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
        text += '\n.\nzestaw infuzyjny: nie udało się zczytać danych'

    try:
        """calculate"""
        sensor = timedelta(hours=SENSOR_ALERT_FREQUENCY)
        if type(sensor_date) == str:
            sensor_alert_date = datetime.strptime(sensor_date[:-6], "%Y-%m-%dT%H:%M:%S") + sensor
            sensor_time_remains = sensor_alert_date - datetime.utcnow()
        else:
            sensor_alert_date = sensor_date + sensor
            sensor_time_remains = sensor_alert_date - datetime.now(timezone.utc)

        """notify"""
        sdays = sensor_time_remains.days
        shours = round(sensor_time_remains.seconds / 3600)
        smicroseconds = sensor_time_remains.microseconds
        if sdays != 0 or shours != 0 or smicroseconds != 0:
            text += "\n.\n Zmień sensor CGM w {} dni i {} godzin".format(sdays, shours)
    except:
        text += '\n.\nsensor CGM: nie udało się zczytać danych'

    send_message(text)
    create_trigger()

    return render(request, "remider/debug.html",
                  {
                      "idays": idays,
                      "ihours": ihours,
                      "sdays": sdays,
                      "shours": shours,
                  })


def create_trigger():
    fdate = (datetime.utcnow() + timedelta(days=1)).replace(hour=16, minute=0, second=0, microsecond=0).isoformat()

    urll = "https://api.atrigger.com/v1/tasks/create?key={}&secret={}&timeSlice={}&count={}&tag_id=typical&url={}&first={}".format(
        ATRIGGER_KEY, ATRIGGER_SECRET, '1minute', 1,
        'https://{}.herokuapp.com/reminder/?key={}'.format(app_name, SECRET_KEY), fdate)
    api_rq.get(urll)


def file(request):
    file = open("staticfiles/uplouded/ATriggerVerify.txt", "rb")

    return FileResponse(file)


def auth(request):
    if request.method == "POST":
        form = GetSecretForm(request.POST)
        if form.is_valid():
            return redirect("https://{}.herokuapp.com/menu/?key={}".format(app_name, form.cleaned_data['apisecret']))
    else:
        form = GetSecretForm()

    return render(request, "remider/auth.html", context={"form": form})


@secret_key_required
def menu(request):
    try:
        info = request.GET.get("info", "")
    except:
        info = False
    info2 = False
    forms_list = []

    if request.method == "POST":
        if 'ns_link_button' in request.POST:
            ns_form, forms_list = create_changeenvvarform('ns_link_button', "NIGHTSCOUT_LINK",
                                                          forms_list, nightscout_link, request.POST)
            if ns_form.is_valid():
                ns_form, forms_list, info2 = save_changeenvvarform(ns_form, 'ns_link_button',
                                                                   "NIGHTSCOUT_LINK", forms_list)
            infusion_freq_form, forms_list = create_changeenvvarform('infusion_freq_button',
                                                                     "INFUSION_SET_ALERT_FREQUENCY",
                                                                     forms_list, INFUSION_SET_ALERT_FREQUENCY, )
            sensor_freq_form, forms_list = create_changeenvvarform('sensor_freq_button', "SENSOR_ALERT_FREQUENCY",
                                                                   forms_list, SENSOR_ALERT_FREQUENCY, )
            twilio_sid_form, forms_list = create_changeenvvarform('twilio_sid_button', "TWILIO_ACCOUNT_SID",
                                                                  forms_list, TWILIO_ACCOUNT_SID)
            twilio_token_form, forms_list = create_changeenvvarform('twilio_token_button', "TWILIO_AUTH_TOKEN",
                                                                    forms_list, TWILIO_AUTH_TOKEN)
            atrigger_key_form, forms_list = create_changeenvvarform('atrigger_key_button', "ATRIGGER_KEY",
                                                                    forms_list, ATRIGGER_KEY)
            atrigger_secret_form, forms_list = create_changeenvvarform('atrigger_secret_button', "ATRIGGER_SECRET",
                                                                       forms_list, ATRIGGER_SECRET)
        if 'infusion_freq_button' in request.POST:
            ns_form, forms_list = create_changeenvvarform('ns_link_button', "NIGHTSCOUT_LINK",
                                                          forms_list, nightscout_link)
            infusion_freq_form, forms_list = create_changeenvvarform('infusion_freq_button',
                                                                     "INFUSION_SET_ALERT_FREQUENCY", forms_list,
                                                                     INFUSION_SET_ALERT_FREQUENCY,
                                                                     request.POST)
            if infusion_freq_form.is_valid():
                infusion_freq_form, forms_list, info2 = save_changeenvvarform(infusion_freq_form,
                                                                              'infusion_freq_button',
                                                                              "INFUSION_SET_ALERT_FREQUENCY",
                                                                              forms_list)

            sensor_freq_form, forms_list = create_changeenvvarform('sensor_freq_button', "SENSOR_ALERT_FREQUENCY",
                                                                   forms_list, SENSOR_ALERT_FREQUENCY, )
            twilio_sid_form, forms_list = create_changeenvvarform('twilio_sid_button', "TWILIO_ACCOUNT_SID",
                                                                  forms_list, TWILIO_ACCOUNT_SID)
            twilio_token_form, forms_list = create_changeenvvarform('twilio_token_button', "TWILIO_AUTH_TOKEN",
                                                                    forms_list, TWILIO_AUTH_TOKEN)
            atrigger_key_form, forms_list = create_changeenvvarform('atrigger_key_button', "ATRIGGER_KEY",
                                                                    forms_list, ATRIGGER_KEY)
            atrigger_secret_form, forms_list = create_changeenvvarform('atrigger_secret_button', "ATRIGGER_SECRET",
                                                                       forms_list, ATRIGGER_SECRET)
        if 'sensor_freq_button' in request.POST:
            ns_form, forms_list = create_changeenvvarform('ns_link_button', "NIGHTSCOUT_LINK",
                                                          forms_list, nightscout_link, )
            infusion_freq_form, forms_list = create_changeenvvarform('infusion_freq_button',
                                                                     "INFUSION_SET_ALERT_FREQUENCY",
                                                                     forms_list, INFUSION_SET_ALERT_FREQUENCY, )

            sensor_freq_form, forms_list = create_changeenvvarform('sensor_freq_button', "SENSOR_ALERT_FREQUENCY",
                                                                   forms_list, SENSOR_ALERT_FREQUENCY, request.POST)
            if sensor_freq_form.is_valid():
                sensor_freq_form, forms_list, info2 = save_changeenvvarform(sensor_freq_form, 'sensor_freq_button',
                                                                            "SENSOR_ALERT_FREQUENCY", forms_list)

            twilio_sid_form, forms_list = create_changeenvvarform('twilio_sid_button', "TWILIO_ACCOUNT_SID",
                                                                  forms_list, TWILIO_ACCOUNT_SID)
            twilio_token_form, forms_list = create_changeenvvarform('twilio_token_button', "TWILIO_AUTH_TOKEN",
                                                                    forms_list, TWILIO_AUTH_TOKEN)
            atrigger_key_form, forms_list = create_changeenvvarform('atrigger_key_button', "ATRIGGER_KEY",
                                                                    forms_list, ATRIGGER_KEY)
            atrigger_secret_form, forms_list = create_changeenvvarform('atrigger_secret_button', "ATRIGGER_SECRET",
                                                                       forms_list, ATRIGGER_SECRET)
        if 'twilio_sid_button' in request.POST:
            ns_form, forms_list = create_changeenvvarform('ns_link_button', "NIGHTSCOUT_LINK",
                                                          forms_list, nightscout_link)
            infusion_freq_form, forms_list = create_changeenvvarform('infusion_freq_button',
                                                                     "INFUSION_SET_ALERT_FREQUENCY",
                                                                     forms_list, INFUSION_SET_ALERT_FREQUENCY, )
            sensor_freq_form, forms_list = create_changeenvvarform('sensor_freq_button', "SENSOR_ALERT_FREQUENCY",
                                                                   forms_list, SENSOR_ALERT_FREQUENCY, )

            twilio_sid_form, forms_list = create_changeenvvarform('twilio_sid_button', "TWILIO_ACCOUNT_SID",
                                                                  forms_list, TWILIO_ACCOUNT_SID, request.POST)
            if twilio_sid_form.is_valid():
                twilio_sid_form, forms_list, info2 = save_changeenvvarform(twilio_sid_form, 'twilio_sid_button',
                                                                           "TWILIO_ACCOUNT_SID", forms_list)

            twilio_token_form, forms_list = create_changeenvvarform('twilio_token_button', "TWILIO_AUTH_TOKEN",
                                                                    forms_list, TWILIO_AUTH_TOKEN)
            atrigger_key_form, forms_list = create_changeenvvarform('atrigger_key_button', "ATRIGGER_KEY",
                                                                    forms_list, ATRIGGER_KEY)
            atrigger_secret_form, forms_list = create_changeenvvarform('atrigger_secret_button', "ATRIGGER_SECRET",
                                                                       forms_list, ATRIGGER_SECRET)
        if 'twilio_token_button' in request.POST:
            ns_form, forms_list = create_changeenvvarform('ns_link_button', "NIGHTSCOUT_LINK",
                                                          forms_list, nightscout_link)
            infusion_freq_form, forms_list = create_changeenvvarform('infusion_freq_button',
                                                                     "INFUSION_SET_ALERT_FREQUENCY",
                                                                     forms_list, INFUSION_SET_ALERT_FREQUENCY, )
            sensor_freq_form, forms_list = create_changeenvvarform('sensor_freq_button', "SENSOR_ALERT_FREQUENCY",
                                                                   forms_list, SENSOR_ALERT_FREQUENCY, )

            twilio_sid_form, forms_list = create_changeenvvarform('twilio_sid_button', "TWILIO_ACCOUNT_SID",
                                                                  forms_list, TWILIO_ACCOUNT_SID)
            twilio_token_form, forms_list = create_changeenvvarform('twilio_token_button', "TWILIO_AUTH_TOKEN",
                                                                    forms_list, TWILIO_AUTH_TOKEN, request.POST)
            if twilio_token_form.is_valid():
                twilio_token_form, forms_list, info2 = save_changeenvvarform(twilio_token_form, 'twilio_token_button',
                                                                             "TWILIO_AUTH_TOKEN", forms_list)

            atrigger_key_form, forms_list = create_changeenvvarform('atrigger_key_button', "ATRIGGER_KEY",
                                                                    forms_list, ATRIGGER_KEY)
            atrigger_secret_form, forms_list = create_changeenvvarform('atrigger_secret_button', "ATRIGGER_SECRET",
                                                                       forms_list, ATRIGGER_SECRET)
        if 'atrigger_key_button' in request.POST:
            ns_form, forms_list = create_changeenvvarform('ns_link_button', "NIGHTSCOUT_LINK",
                                                          forms_list, nightscout_link)
            infusion_freq_form, forms_list = create_changeenvvarform('infusion_freq_button',
                                                                     "INFUSION_SET_ALERT_FREQUENCY",
                                                                     forms_list, INFUSION_SET_ALERT_FREQUENCY, )
            sensor_freq_form, forms_list = create_changeenvvarform('sensor_freq_button', "SENSOR_ALERT_FREQUENCY",
                                                                   forms_list, SENSOR_ALERT_FREQUENCY, )

            twilio_sid_form, forms_list = create_changeenvvarform('twilio_sid_button', "TWILIO_ACCOUNT_SID",
                                                                  forms_list, TWILIO_ACCOUNT_SID)
            twilio_token_form, forms_list = create_changeenvvarform('twilio_token_button', "TWILIO_AUTH_TOKEN",
                                                                    forms_list, TWILIO_AUTH_TOKEN)
            atrigger_key_form, forms_list = create_changeenvvarform('atrigger_key_button', "ATRIGGER_KEY",
                                                                    forms_list, ATRIGGER_KEY, request.POST)
            if atrigger_key_form.is_valid():
                atrigger_key_form, forms_list, info2 = save_changeenvvarform(atrigger_key_form, 'atrigger_key_button',
                                                                             "ATRIGGER_KEY", forms_list)

            atrigger_secret_form, forms_list = create_changeenvvarform('atrigger_secret_button', "ATRIGGER_SECRET",
                                                                       forms_list, ATRIGGER_SECRET)
        if 'atrigger_secret_button' in request.POST:
            ns_form, forms_list = create_changeenvvarform('ns_link_button', "NIGHTSCOUT_LINK",
                                                          forms_list, nightscout_link)
            infusion_freq_form, forms_list = create_changeenvvarform('infusion_freq_button',
                                                                     "INFUSION_SET_ALERT_FREQUENCY",
                                                                     forms_list, INFUSION_SET_ALERT_FREQUENCY, )
            sensor_freq_form, forms_list = create_changeenvvarform('sensor_freq_button', "SENSOR_ALERT_FREQUENCY",
                                                                   forms_list, SENSOR_ALERT_FREQUENCY, )

            twilio_sid_form, forms_list = create_changeenvvarform('twilio_sid_button', "TWILIO_ACCOUNT_SID",
                                                                  forms_list, TWILIO_ACCOUNT_SID)
            twilio_token_form, forms_list = create_changeenvvarform('twilio_token_button', "TWILIO_AUTH_TOKEN",
                                                                    forms_list, TWILIO_AUTH_TOKEN)
            atrigger_key_form, forms_list = create_changeenvvarform('atrigger_key_button', "ATRIGGER_KEY",
                                                                    forms_list, ATRIGGER_KEY)
            atrigger_secret_form, forms_list = create_changeenvvarform('atrigger_key_button', "ATRIGGER_SECRET",
                                                                       forms_list, ATRIGGER_SECRET, request.POST)
            if atrigger_secret_form.is_valid():
                atrigger_secret_form, forms_list, info2 = save_changeenvvarform(atrigger_secret_form,
                                                                                'atrigger_key_button',
                                                                                "ATRIGGER_SECRET", forms_list)
    else:
        ns_form, forms_list = create_changeenvvarform('ns_link_button', "NIGHTSCOUT_LINK",
                                                      forms_list, nightscout_link)
        infusion_freq_form, forms_list = create_changeenvvarform('infusion_freq_button', "INFUSION_SET_ALERT_FREQUENCY",
                                                                 forms_list, INFUSION_SET_ALERT_FREQUENCY, )
        sensor_freq_form, forms_list = create_changeenvvarform('sensor_freq_button', "SENSOR_ALERT_FREQUENCY",
                                                               forms_list, SENSOR_ALERT_FREQUENCY, )
        twilio_sid_form, forms_list = create_changeenvvarform('twilio_sid_button', "TWILIO_ACCOUNT_SID",
                                                              forms_list, TWILIO_ACCOUNT_SID)
        twilio_token_form, forms_list = create_changeenvvarform('twilio_token_button', "TWILIO_AUTH_TOKEN",
                                                                forms_list, TWILIO_AUTH_TOKEN)
        atrigger_key_form, forms_list = create_changeenvvarform('atrigger_key_button', "ATRIGGER_KEY",
                                                                forms_list, ATRIGGER_KEY)
        atrigger_secret_form, forms_list = create_changeenvvarform('atrigger_secret_button', "ATRIGGER_SECRET",
                                                                   forms_list, ATRIGGER_SECRET)

    return render(request, "remider/menu.html",
                  {'urllink': 'https://{}.herokuapp.com/upload/?key={}'.format(app_name, SECRET_KEY), 'info': info,
                   'forms_list': forms_list, "info2": info2,
                   "urllink2": "https://{}.herokuapp.com/phonenumbers/?key={}".format(app_name, SECRET_KEY)}, )


@secret_key_required
def upload(request):
    if request.method == 'POST':
        form = FileUploudForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            with open('staticfiles/uplouded/ATriggerVerify.txt', 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            return redirect("https://{}.herokuapp.com/menu/?key={}&info={}".format(app_name, SECRET_KEY, True))
    else:
        form = FileUploudForm()
    return render(request, 'remider/upload.html', {'form': form, })


class ManagePhoneNumbersView(TemplateView):
    template_name = "remider/manage_ph.html"
    forms_list = []
    to_numbers_forms_list = {}
    info = (False, "")

    def post(self, request, *args, **kwargs):
        self.to_numbers_forms_list = {}
        self.forms_list = []
        post_data = request.POST
        from_number_form = self.create_changeenvvarform('from_number_button', "NUMBER OF SENDER", from_number,
                                                        post_data)

        for i, number in enumerate(to_numbers):
            label = "to_number_" + str(i + 1)
            button_name = label + "_button"
            label_tag = "RECEIVING NUMBER " + str(i + 1) + "."
            form = self.create_changeenvvarform(button_name, label_tag, number, post_data)
            self.to_numbers_forms_list[label] = form
        next_number_id = len(to_numbers) + 1
        new_number_form = self.create_changeenvvarform('new_number_button',
                                                       "RECEIVING NUMBER" + str(next_number_id) + ".", "", post_data)

        if from_number_form.is_valid() and 'from_number_button' in post_data:
            from_number_form, self.info = self.save_changeenvvarform(from_number_form, "from_number", )

        for i, number in enumerate(to_numbers):
            label = "to_number_" + str(i + 1)
            button_name = label + "_button"
            form = self.to_numbers_forms_list[label]
            if form.is_valid() and button_name in post_data:
                form, self.info = self.save_changeenvvarform(form, label)
                break

        if new_number_form.is_valid() and 'new_number_button' in post_data:
            new_number_form, self.info = self.save_changeenvvarform(new_number_form, "to_number_" + str(next_number_id))
        contex = self.get_context_data(forms_list=self.forms_list, info=self.info, delinfo=(False, ""),
                                       delurl=self.delurl)

        return self.render_to_response(contex)

    def get(self, request, *args, **kwargs):
        try:
            delinfo = (request.GET.get("delinfo", ""), request.GET.get("delid", ""))
            if delinfo[0]:
                label = "to_number_" + str(delinfo[1])
                form = self.to_numbers_forms_list.pop(label)
                self.forms_list.remove(form)
                self.forms_list[-2].deletable = True

        except:
            delinfo = (False, "")

        self.forms_list = []
        self.to_numbers_forms_list = {}
        self.create_changeenvvarform('from_number_button', "NUMBER OF SENDER", from_number)

        for i, number in enumerate(to_numbers):
            label = "to_number_" + str(i + 1)
            button_name = label + "_button"
            label_tag = "RECEIVING NUMBER " + str(i + 1) + "."
            form = self.create_changeenvvarform(button_name, label_tag, number)
            self.to_numbers_forms_list[label] = form

        next_number_id = len(to_numbers) + 1
        self.create_changeenvvarform('new_number_button', "RECEIVING NUMBER" + str(next_number_id) + ".", "")
        contex = self.get_context_data(forms_list=self.forms_list, info=self.info, delinfo=delinfo, delurl=self.delurl)

        return self.render_to_response(contex)

    def create_changeenvvarform(self, button_name, label, default, post_data=()):
        if button_name in post_data:
            form = ChangeEnvVariableForm(post_data)
        else:
            form = ChangeEnvVariableForm()

        form.button_name = button_name
        form.fields['new_value'].label = label
        form.fields['new_value'].initial = default
        form.fields["new_value"].required = False
        if form.button_name == 'new_number_button':
            form.action = "ADD"
            self.forms_list[-1].deletable = True
            id = len(self.to_numbers_forms_list)
            self.delurl = "https://{}.herokuapp.com/deletephonenumber/{}/?key={}".format(app_name, id, SECRET_KEY)
        else:
            form.action = "CHANGE"

        self.forms_list.append(form)
        return form

    def save_changeenvvarform(self, form, label):
        var = form.cleaned_data["new_value"]
        change_config_var(label, var)
        if form.button_name == 'new_number_button':
            action = "ADDED"
            self.forms_list[-2].deletable = False
            form.action = "CHANGE"
            form.button_name = label + "_button"
            self.to_numbers_forms_list[label] = form
            next_number_id = len(self.to_numbers_forms_list) + 1
            self.create_changeenvvarform('new_number_button', "RECEIVING NUMBER" + str(next_number_id) + ".", "")


        else:
            action = "CHANGED"
        info2 = (True, form.fields['new_value'].label, action)

        return form, info2


@secret_key_required
def delete_view(request, number_id):
    label = "to_number_" + str(number_id)
    change_config_var(label, None)

    return redirect(
        "https://{}.herokuapp.com/phonenumbers/?key={}&delinfo={}&delid={}".format(app_name, SECRET_KEY, True,
                                                                                   number_id))
