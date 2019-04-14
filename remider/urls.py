from django.urls import path
from .views import reminder_view, home, file, auth, menu, upload, manage_ph_numbers
urlpatterns = [
    path("", home, name="home"),
    path("reminder/", reminder_view, name="reminder"),
    path("ATriggerVerify.txt",file),
    path("auth/", auth, name='get_secret'),
    path("menu/", menu, name='menu'),
    path("upload/", upload, name="upload"),
    path("phonenumbers/", manage_ph_numbers, name="manage_ph_numbers"),

]
