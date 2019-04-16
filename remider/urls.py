from django.urls import path
from django.views.generic import TemplateView
from .views import reminder_view, file, auth, menu, upload, manage_ph_numbers, ManagePhoneNumbersView
from .decorators import secret_key_required

urlpatterns = [
    path("", TemplateView.as_view(template_name="remider/home.html"), name="home"),
    path("reminder/", reminder_view, name="reminder"),
    path("ATriggerVerify.txt", file),
    path("auth/", auth, name='get_secret'),
    path("menu/", menu, name='menu'),
    path("upload/", upload, name="upload"),
    path("phonenumbers/", secret_key_required(ManagePhoneNumbersView.as_view()), name="manage_ph_numbers"),

]
