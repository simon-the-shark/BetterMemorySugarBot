from bootstrap_datepicker_plus import TimePickerInput
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .models import TriggerTime


class GetSecretForm(forms.Form):
    """ authorization form """
    apisecret = forms.CharField(required=True, widget=forms.PasswordInput, label='SECRET_KEY')


class FileUploudForm(forms.Form):
    """ form for uplouding files """
    file = forms.FileField()


class ChangeEnvVariableForm(forms.Form):
    """ form for changing envinronment variables """
    button_name = ""
    deletable = False
    new_value = forms.CharField(required=True)


class ChooseNotificationsWayForm(forms.Form):
    """ form for choosing notifications way """
    ifttt_notifications = forms.BooleanField(required=False, label=_("TRIGGER IFTTT (SEND WEBHOOKS)"))
    sms_notifications = forms.BooleanField(required=False, label=_("SEND SMS"))


class ChooseLanguageForm(forms.Form):
    """ form for choosing your language """
    language = forms.ChoiceField(required=True, choices=settings.LANGUAGES,
                                 label=_("LANGUAGE"))


class TriggerTimeForm(forms.ModelForm):
    """ form for changing waking up time """

    class Meta:
        model = TriggerTime
        fields = ["time"]
        labels = {"time": _("NOTIFICATION TIME. Please give UTC TIME"), }
        widgets = {"time": TimePickerInput(), }
