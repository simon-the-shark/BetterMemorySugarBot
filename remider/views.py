import sys

import requests
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView

from infusionset_reminder.settings import SENSOR_ALERT_FREQUENCY, INFUSION_SET_ALERT_FREQUENCY, ATRIGGER_KEY, \
    ATRIGGER_SECRET, SECRET_KEY, app_name, nightscout_link, TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_SID, from_number, \
    to_numbers, ifttt_makers, trigger_ifttt, send_sms
from .api_interactions import change_config_var, create_trigger, notify
from .data_processing import process_nightscouts_api_response, calculate_infusion, calculate_sensor, \
    get_sms_txt_infusion_set, get_sms_txt_sensor
from .decorators import secret_key_required
from .forms import ChangeEnvVariableForm, ChooseNotificationsWayForm
from .forms import GetSecretForm, FileUploudForm


@secret_key_required
def quiet_checkup_view(request):
    """
    shows remaining time to next change (infusion set or CGM sensor)
    without sending notification
    """
    return reminder_and_notifier_view(request, False)


@secret_key_required
def reminder_and_notifier_view(request, send_notif=True):
    """
    get latest infusion set or CGM sensor change date from Nightscout`s API
    saves it in database
    calculates next change date
    sends notification via sms
    """

    response = requests.get(nightscout_link + "/api/v1/treatments")
    date, sensor_date = process_nightscouts_api_response(response)

    sms_text = ""

    try:
        infusion_time_remains = calculate_infusion(date)
        inf_text = get_sms_txt_infusion_set(infusion_time_remains)
        sms_text += inf_text

    except TypeError:  # date is None
        inf_text = '.\n\nZestaw infuzyjny: nie udało się zczytać danych'
        sms_text += inf_text

    except Exception as error:
        print(error)
        sys.stdout.flush()
        inf_text = '.\n\n Zestaw infuzyjny: nie udało się przetworzyć danych'
        sms_text += inf_text
    try:
        sensor_time_remains = calculate_sensor(sensor_date)
        sensor_text = get_sms_txt_sensor(sensor_time_remains)
        sms_text += sensor_text

    except TypeError:  # sensor_date is None
        sensor_text = '\n\nSensor CGM: nie udało się zczytać danych'
        sms_text += sensor_text

    except Exception as error:
        print(error)
        sys.stdout.flush()
        sensor_text = '\n\nSensor CGM: nie udało się przetworzyć danych'
        sms_text += sensor_text

    if send_notif:
        notify(sms_text)
        create_trigger()

    return render(request, "remider/debug.html",
                  {
                      "inf_text": inf_text[1:],
                      "sensor_text": sensor_text,
                      "menu_url": "https://{}.herokuapp.com/menu/?key={}".format(app_name, SECRET_KEY),
                  })


def file_view(request):
    """
    view returns verification file for atrigger.com
    """
    file = open("staticfiles/uplouded/ATriggerVerify.txt", "rb")

    return FileResponse(file)


def auth_view(request):
    """ authorization view via SECRET_KEY """
    if request.method == "POST":
        form = GetSecretForm(request.POST)
        if form.is_valid():
            return redirect("https://{}.herokuapp.com/menu/?key={}".format(app_name, form.cleaned_data['apisecret']))
    else:
        form = GetSecretForm()

    return render(request, "remider/auth.html", {"form": form})


class MenuView(TemplateView):
    """
    menu view
    redirecting buttons and config variables control
    """
    template_name = "remider/menu.html"

    urllink = 'https://{}.herokuapp.com/upload/?key={}'.format(app_name, SECRET_KEY)
    urllink2 = "https://{}.herokuapp.com/notifications-center/?key={}".format(app_name, SECRET_KEY)
    urllink3 = "https://{}.herokuapp.com/reminder/?key={}".format(app_name, SECRET_KEY)
    urllink4 = "https://{}.herokuapp.com/reminder/quiet/?key={}".format(app_name, SECRET_KEY)

    forms_list = []
    forms = (
        ("NIGHTSCOUT_LINK", "ns_link_button", nightscout_link),
        ("INFUSION_SET_ALERT_FREQUENCY", "infusion_freq_button", INFUSION_SET_ALERT_FREQUENCY),
        ("SENSOR_ALERT_FREQUENCY", "sensor_freq_button", SENSOR_ALERT_FREQUENCY),
        ("TWILIO_ACCOUNT_SID", "twilio_sid_button", TWILIO_ACCOUNT_SID),
        ("TWILIO_AUTH_TOKEN", "twilio_token_button", TWILIO_AUTH_TOKEN),
        ("ATRIGGER_KEY", "atrigger_key_button", ATRIGGER_KEY),
        ("ATRIGGER_SECRET", "atrigger_secret_button", ATRIGGER_SECRET),
    )

    def post(self, request, *args, **kwargs):
        """
        POST method
        handles http`s POST request
        loads forms
        checks if they are submitted
        changes config variables
        """
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
                                       urllink3=self.urllink3, urllink4=self.urllink4, info=self.info, info2=self.info2)
        return self.render_to_response(contex)

    def get(self, request, *args, **kwargs):
        """
        GET method
        handles http`s GET request
        loads forms
        shows info about successful change
        """
        self.forms_list = []
        try:
            self.info = request.GET.get("info", "")
        except:
            self.info = False
        self.info2 = False

        for form_tuple in self.forms:
            self.create_changeenvvarform(form_tuple[1], form_tuple[0], form_tuple[2])

        contex = self.get_context_data(forms_list=self.forms_list, urllink=self.urllink, urllink2=self.urllink2,
                                       urllink3=self.urllink3, urllink4=self.urllink4, info=self.info, info2=self.info2)
        return self.render_to_response(contex)

    def create_changeenvvarform(self, button_name, label, default, post_data=()):
        """
         creates form and adds it to forms_list
        :param button_name: string, unique button name
        :param label: string, field`s display name
        :param default: string, default value of form`s field
        :param post_data: request.POST or empty tuple
        :return: ready to use form
        """
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
        """
        reads data from submitted form and changes config variables
        :param form: submitted form
        :param label: name of config variable
        :return: already used form and info about successful change
        """
        var = form.cleaned_data["new_value"]
        change_config_var(label, var)
        info2 = (True, label)

        return form, info2


@secret_key_required
def upload_view(request):
    """ allows user to upload verification file for atrigger.com """
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
    """
    allows user to change, add or delete his phone numbers
    """
    template_name = "remider/manage_ph.html"
    forms_list = []
    to_numbers_forms_list = {}
    info = (False, "")
    menu_url = "https://{}.herokuapp.com/menu/?key={}".format(app_name, SECRET_KEY)

    def post(self, request, *args, **kwargs):
        """
        GET method
        handles http`s GET request
        loads forms
        shows info about successful change
        """
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
        """
        GET method
        handles http`s GET request
        loads forms
        shows info about successful change
        """
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
        """
        creates form and adds it to forms_list
        :param button_name: string, unique button name
        :param label: string, field`s display name
        :param default: string, default value of form`s field
        :param post_data: request.POST or empty tuple
        :return: ready to use form
        """
        if button_name in post_data:
            form = ChangeEnvVariableForm(post_data)
        else:
            form = ChangeEnvVariableForm()

        form.button_name = button_name
        form.fields['new_value'].label = label
        form.fields['new_value'].initial = default
        form.fields["new_value"].required = False
        if form.button_name == 'new_number_button':  # special treatment for adding new number form
            form.action = "ADD"
            if len(self.forms_list) > 0:
                self.forms_list[-1].deletable = True
            id = len(self.to_numbers_forms_list)
            self.delurl = "https://{}.herokuapp.com/deletephonenumber/{}/?key={}".format(app_name, id, SECRET_KEY)
        else:
            form.action = "CHANGE"

        self.forms_list.append(form)
        return form

    def save_changeenvvarform(self, form, label):
        """
        reads data from submitted form and changes config variables
        :param form: submitted form
        :param label: name of config variable
        :return: already used form and info about successful change
        """
        var = form.cleaned_data["new_value"]
        change_config_var(label, var)
        if form.button_name == 'new_number_button':  # special treatment for adding new number form
            action = "ADDED"
            if len(self.forms_list) > 1:
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
def number_delete_view(request, number_id):
    """
     view handles requests for phone number deleting
    :param request: http request
    :param number_id: assigned number of phone number (requested to deleting)
    :return: redirects to phone numbers management view
    """
    label = "to_number_" + str(number_id)
    change_config_var(label, None)

    return redirect(
        "https://{}.herokuapp.com/phonenumbers/?key={}&delinfo={}&delid={}".format(app_name, SECRET_KEY, True,
                                                                                   number_id))


@secret_key_required
def ifttt_delete_view(request, maker_id):
    """
     view handles requests for IFTTT makers deleting
    :param request: http request
    :param maker_id: assigned number of IFTTT maker (requested to deleting)
    :return: redirects to IFTTT makers management view
    """
    label = "IFTTT_MAKER_" + str(maker_id)
    change_config_var(label, None)

    return redirect(
        "https://{}.herokuapp.com/iftttmakers/?key={}&delinfo={}&delid={}".format(app_name, SECRET_KEY, True,
                                                                                  maker_id))


class NotificationsCenterView(FormView):
    """
    view for notifications management
    """
    form_class = ChooseNotificationsWayForm
    template_name = "remider/notifications.html"

    urllink = "https://{}.herokuapp.com/iftttmakers/?key={}".format(app_name, SECRET_KEY)
    urllink2 = "https://{}.herokuapp.com/phonenumbers/?key={}".format(app_name, SECRET_KEY)

    def get_initial(self):
        """
        :return: initial values for form
        """
        initial = super(NotificationsCenterView, self).get_initial()
        initial["ifttt_notifications"] = trigger_ifttt
        initial["sms_notifications"] = send_sms

        return initial

    def get_context_data(self, **kwargs):
        """
        :return: contex data
        """
        return super().get_context_data(**kwargs, urllink=self.urllink, urllink2=self.urllink2, )

    def form_valid(self, form):
        """
        method for handling validly submitted forms
        """
        ifttt = form.cleaned_data["ifttt_notifications"]
        sms = form.cleaned_data["sms_notifications"]
        change_config_var("trigger_ifttt", ifttt)
        change_config_var("send_sms", sms)
        form.fields["ifttt_notifications"].initial = ifttt
        form.fields["sms_notifications"].initial = sms

        return self.render_to_response(self.get_context_data())


class ManageIFTTTMakersView(TemplateView):
    """
    view for adding, changing and deleting IFTTT makers
    """
    template_name = "remider/manage_ifttt.html"
    forms_list = []
    makers_dict = {}
    info = (False, "")
    menu_url = "https://{}.herokuapp.com/menu/?key={}".format(app_name, SECRET_KEY)

    def post(self, request, *args, **kwargs):
        """
        GET method
        handles http`s GET request
        loads forms
        shows info about successful change
        """
        self.makers_dict = {}
        self.forms_list = []
        post_data = request.POST

        for i, maker in enumerate(ifttt_makers):
            label = "IFTTT_MAKER_" + str(i + 1)
            button_name = label + "_button"
            label_tag = "IFTTT MAKER " + str(i + 1) + "."
            form = self.create_changeenvvarform(button_name, label_tag, maker, post_data)
            self.makers_dict[label] = form
        next_maker_id = len(ifttt_makers) + 1
        new_maker_form = self.create_changeenvvarform('new_maker_button',
                                                      "IFTTT MAKER " + str(next_maker_id) + ".", "", post_data)

        for i, maker in enumerate(ifttt_makers):
            label = "IFTTT_MAKER_" + str(i + 1)
            button_name = label + "_button"
            form = self.makers_dict[label]
            if form.is_valid() and button_name in post_data:
                form, self.info = self.save_changeenvvarform(form, label)
                break

        if new_maker_form.is_valid() and 'new_maker_button' in post_data:
            new_maker_form, self.info = self.save_changeenvvarform(new_maker_form, "IFTTT_MAKER_" + str(next_maker_id))
        contex = self.get_context_data(forms_list=self.forms_list, info=self.info, delinfo=(False, ""),
                                       delurl=self.delurl, menu_url=self.menu_url, )

        return self.render_to_response(contex)

    def get(self, request, *args, **kwargs):
        """
        GET method
        handles http`s GET request
        loads forms
        shows info about successful change
        """
        try:
            delinfo = (request.GET.get("delinfo", ""), request.GET.get("delid", ""))
        except:
            delinfo = (False, "")

        self.forms_list = []
        self.makers_dict = {}

        for i, maker in enumerate(ifttt_makers):
            label = "IFTTT_MAKER_" + str(i + 1)
            button_name = label + "_button"
            label_tag = "IFTTT MAKER " + str(i + 1) + "."
            form = self.create_changeenvvarform(button_name, label_tag, maker)
            self.makers_dict[label] = form

        next_maker_id = len(ifttt_makers) + 1
        self.create_changeenvvarform('new_maker_button', "IFTTT MAKER " + str(next_maker_id) + ".", "")

        if delinfo[0]:
            id = delinfo[1]
            label = "IFTTT_MAKER_" + str(id)
            form = self.makers_dict.pop(label)
            self.forms_list.remove(form)
            self.forms_list[-2].deletable = True
            self.delurl = "https://{}.herokuapp.com/deletemaker/{}/?key={}".format(app_name, str(int(id) - 1),
                                                                                   SECRET_KEY)
            self.forms_list[-1].fields["new_value"].label = "IFTTT MAKER " + str(
                len(self.makers_dict) + 1) + "."
        contex = self.get_context_data(forms_list=self.forms_list, info=self.info, delinfo=delinfo, delurl=self.delurl,
                                       menu_url=self.menu_url, )

        return self.render_to_response(contex)

    def create_changeenvvarform(self, button_name, label, default, post_data=()):
        """
        creates form and adds it to forms_list
        :param button_name: string, unique button name
        :param label: string, field`s display name
        :param default: string, default value of form`s field
        :param post_data: request.POST or empty tuple
        :return: ready to use form
        """
        if button_name in post_data:
            form = ChangeEnvVariableForm(post_data)
        else:
            form = ChangeEnvVariableForm()

        form.button_name = button_name
        form.fields['new_value'].label = label
        form.fields['new_value'].initial = default
        form.fields["new_value"].required = False
        if form.button_name == 'new_maker_button':  # special treatment for adding new maker form
            form.action = "ADD"
            if len(self.forms_list) > 0:
                self.forms_list[-1].deletable = True
            id = len(self.makers_dict)
            self.delurl = "https://{}.herokuapp.com/deletemaker/{}/?key={}".format(app_name, id, SECRET_KEY)
        else:
            form.action = "CHANGE"

        self.forms_list.append(form)
        return form

    def save_changeenvvarform(self, form, label):
        """
        reads data from submitted form and changes config variables
        :param form: submitted form
        :param label: name of config variable
        :return: already used form and info about successful change
        """
        var = form.cleaned_data["new_value"]
        change_config_var(label, var)
        if form.button_name == 'new_maker_button':  # special treatment for adding new maker form
            action = "ADDED"
            if len(self.forms_list) > 1:
                self.forms_list[-2].deletable = False
            form.action = "CHANGE"
            form.button_name = label + "_button"
            self.makers_dict[label] = form
            next_maker_id = len(self.makers_dict) + 1
            self.create_changeenvvarform('new_maker_button', "IFTTT MAKER " + str(next_maker_id) + ".", "")


        else:
            action = "CHANGED"
        info2 = (True, form.fields['new_value'].label, action)

        return form, info2
