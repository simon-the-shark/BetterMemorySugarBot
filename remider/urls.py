from django.urls import re_path
from django.views.generic import TemplateView

from .views import reminder_view, file, auth, menu, upload, ManagePhoneNumbersView
from .decorators import secret_key_required

urlpatterns = [
    re_path(r"^$", TemplateView.as_view(template_name="remider/home.html"), name="home"),
    re_path(r"^reminder/$", reminder_view, name="reminder"),
    re_path(r"^ATriggerVerify.txt$", file),
    re_path(r"^auth/$", auth, name='get_secret'),
    re_path(r"^menu/$", menu, name='menu'),
    re_path(r"^upload/$", upload, name="upload"),
    re_path(r"^phonenumbers/$", secret_key_required(ManagePhoneNumbersView.as_view()), name="manage_ph_numbers"),

]
