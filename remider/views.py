from django.shortcuts import render, redirect
from django.http import FileResponse
from django.views.generic import TemplateView

import requests
from datetime import datetime, timedelta, timezone

from .forms import GetSecretForm, FileUploudForm
from infusionset_reminder.settings import SENSOR_ALERT_FREQUENCY, INFUSION_SET_ALERT_FREQUENCY, ATRIGGER_KEY, \
    ATRIGGER_SECRET, SECRET_KEY, app_name, nightscout_link, TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_SID, from_number, \
    to_numbers
from .models import InfusionChanged, SensorChanged
from .forms import ChangeEnvVariableForm
from .decorators import secret_key_required
from .api_interactions import send_message, change_config_var, create_trigger


@secret_key_required
def quiet_checkup_view(request):
    return reminder_and_notifier_view(request, False)


@secret_key_required
def reminder_and_notifier_view(request, send_notif=True):
    """get_from_api"""
    date = None
    sensor_date = None
    r = requests.get(nightscout_link + "/api/v1/treatments")
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
            infusion_time_remains = infusion_alert_date - datetime.utcnow()

        else:
            infusion_alert_date = date + infusion
            infusion_time_remains = infusion_alert_date - datetime.now(timezone.utc)

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
    if send_notif:
        send_message(text)
        create_trigger()

    return render(request, "remider/debug.html",
                  {
                      "idays": idays,
                      "ihours": ihours,
                      "sdays": sdays,
                      "shours": shours,
                      "menu_url": "https://{}.herokuapp.com/menu/?key={}".format(app_name, SECRET_KEY),
                  })


def file_view(request):
    file = open("staticfiles/uplouded/ATriggerVerify.txt", "rb")

    return FileResponse(file)


def auth_view(request):
    if request.method == "POST":
        form = GetSecretForm(request.POST)
        if form.is_valid():
            return redirect("https://{}.herokuapp.com/menu/?key={}".format(app_name, form.cleaned_data['apisecret']))
    else:
        form = GetSecretForm()

    return render(request, "remider/auth.html", {"form": form})


class MenuView(TemplateView):
    template_name = "remider/menu.html"

    urllink = 'https://{}.herokuapp.com/upload/?key={}'.format(app_name, SECRET_KEY)
    urllink2 = "https://{}.herokuapp.com/phonenumbers/?key={}".format(app_name, SECRET_KEY)
    urllink3 = "https://{}.herokuapp.com/reminder/?key={}".format(app_name, SECRET_KEY)
    urllink4 = "https://{}.herokuapp.com/reminder/quiet/?key={}".format(app_name, SECRET_KEY)

    forms_list = []
    forms = [
        ("NIGHTSCOUT_LINK", "ns_link_button", nightscout_link),
        ("INFUSION_SET_ALERT_FREQUENCY", "infusion_freq_button", INFUSION_SET_ALERT_FREQUENCY),
        ("SENSOR_ALERT_FREQUENCY", "sensor_freq_button", SENSOR_ALERT_FREQUENCY),
        ("TWILIO_ACCOUNT_SID", "twilio_sid_button", TWILIO_ACCOUNT_SID),
        ("TWILIO_AUTH_TOKEN", "twilio_token_button", TWILIO_AUTH_TOKEN),
        ("ATRIGGER_KEY", "atrigger_key_button", ATRIGGER_KEY),
        ("ATRIGGER_SECRET", "atrigger_secret_button", ATRIGGER_SECRET),
    ]

    def post(self, request, *args, **kwargs):
        self.info = False
        self.info2 = False
        self.forms_list = []
        self.forms_link_dict = {}
        post_data = request.POST or None

        for form_tuple in self.forms:
            form = self.create_changeenvvarform(form_tuple[1], form_tuple[0], form_tuple[2], post_data)
            self.forms_link_dict[form_tuple[0]] = form

        for form_tuple in self.forms:
            form = self.forms_link_dict[form_tuple[0]]
            if form.is_valid() and form_tuple[1] in post_data:
                form, self.info2 = self.save_changeenvvarform(form, form_tuple[0])

        contex = self.get_context_data(forms_list=self.forms_list, urllink=self.urllink, urllink2=self.urllink2,
                                       info=self.info, info2=self.info2)
        return self.render_to_response(contex)

    def get(self, request, *args, **kwargs):
        self.forms_list = []
        try:
            self.info = request.GET.get("info", "")
        except:
            self.info = False
        self.info2 = False

        for form_tuple in self.forms:
            self.create_changeenvvarform(form_tuple[1], form_tuple[0], form_tuple[2])

        contex = self.get_context_data(forms_list=self.forms_list, urllink=self.urllink, urllink2=self.urllink2,
                                       info=self.info, info2=self.info2)
        return self.render_to_response(contex)

    def create_changeenvvarform(self, button_name, label, default, post_data=()):
        if button_name in post_data:
            form = ChangeEnvVariableForm(post_data)
        else:
            form = ChangeEnvVariableForm()
        form.button_name = button_name
        form.fields['new_value'].label = label
        form.fields['new_value'].initial = default
        self.forms_list.append(form)
        return form

    def save_changeenvvarform(self, form, label):
        var = form.cleaned_data["new_value"]
        change_config_var(label, var)
        info2 = (True, label)

        return form, info2


@secret_key_required
def upload_view(request):
    menu_url = "https://{}.herokuapp.com/menu/?key={}".format(app_name, SECRET_KEY)
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
    return render(request, 'remider/upload.html', {'form': form, "menu_url": menu_url, })


class ManagePhoneNumbersView(TemplateView):
    template_name = "remider/manage_ph.html"
    forms_list = []
    to_numbers_forms_list = {}
    info = (False, "")
    menu_url = "https://{}.herokuapp.com/menu/?key={}".format(app_name, SECRET_KEY)

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
                                       delurl=self.delurl, menu_url=self.menu_url, )

        return self.render_to_response(contex)

    def get(self, request, *args, **kwargs):
        try:
            delinfo = (request.GET.get("delinfo", ""), request.GET.get("delid", ""))


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
        self.create_changeenvvarform('new_number_button', "RECEIVING NUMBER " + str(next_number_id) + ".", "")

        if delinfo[0]:
            id = delinfo[1]
            label = "to_number_" + str(id)
            form = self.to_numbers_forms_list.pop(label)
            self.forms_list.remove(form)
            self.forms_list[-2].deletable = True
            self.delurl = "https://{}.herokuapp.com/deletephonenumber/{}/?key={}".format(app_name, str(int(id) - 1),
                                                                                         SECRET_KEY)
            self.forms_list[-1].fields["new_value"].label = "RECEIVING NUMBER" + str(
                len(self.to_numbers_forms_list) + 1) + "."
        contex = self.get_context_data(forms_list=self.forms_list, info=self.info, delinfo=delinfo, delurl=self.delurl,
                                       menu_url=self.menu_url, )

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
            self.create_changeenvvarform('new_number_button', "RECEIVING NUMBER " + str(next_number_id) + ".", "")


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
