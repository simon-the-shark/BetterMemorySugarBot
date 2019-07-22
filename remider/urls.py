from django.urls import re_path
from django.views.generic import TemplateView

from .decorators import secret_key_required, set_language_to_LANGUAGE_CODE
from .views import reminder_and_notifier_view, file_view, auth_view, upload_view, ManagePhoneNumbersView, \
    number_delete_view, MenuView, quiet_checkup_view, NotificationsCenterView, ManageIFTTTMakersView, ifttt_delete_view

urlpatterns = [
    re_path(r"^$", set_language_to_LANGUAGE_CODE(TemplateView.as_view(template_name="remider/home.html")), name="home"),
    re_path(r"^reminder/$", reminder_and_notifier_view, name="reminder"),
    re_path(r"^ATriggerVerify.txt$", file_view, name="atriggerfile"),
    re_path(r"^auth/$", auth_view, name='get_secret'),
    re_path(r"^menu/$", secret_key_required(set_language_to_LANGUAGE_CODE(MenuView.as_view())), name='menu'),
    re_path(r"^upload/$", upload_view, name="upload"),
    re_path(r"^phonenumbers/$", secret_key_required(set_language_to_LANGUAGE_CODE(ManagePhoneNumbersView.as_view())),
            name="manage_ph_numbers"),
    re_path(r"^deletephonenumber/(?P<number_id>[0-9]+)/$", number_delete_view, name="del-ph"),
    re_path(r"^reminder/quiet/$", quiet_checkup_view, name="quiet"),
    re_path(r"^notifications-center/$",
            secret_key_required(set_language_to_LANGUAGE_CODE(NotificationsCenterView.as_view())), name="notif-center"),
    re_path(r"^iftttmakers/$", secret_key_required(set_language_to_LANGUAGE_CODE(ManageIFTTTMakersView.as_view())),
            name='manage_ifttt_makers'),
    re_path(r"^deletemaker/(?P<maker_id>[0-9]+)/$", ifttt_delete_view, name="del-ifttt"),

]
