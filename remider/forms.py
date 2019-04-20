from django import forms

from infusionset_reminder.settings import trigger_ifttt, send_sms


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
    ifttt_notifications = forms.BooleanField(initial=trigger_ifttt, required=False,
                                             label="TRIGGER IFTTT (SEND WEBHOOKS)")
    sms_notifications = forms.BooleanField(initial=send_sms, required=False, label="SEND SMS NOTIFICATIONS")
