from django import forms

from .languages import *


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
    ifttt_notifications = forms.BooleanField(required=False, label=languages_ifttt_label)
    sms_notifications = forms.BooleanField(required=False, label=languages_sms_label)
