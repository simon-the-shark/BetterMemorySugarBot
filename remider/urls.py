from django.urls import path
from .views import reminder_view, home, file, auth, menu, upload
urlpatterns = [
    path("", home),
    path("reminder/", reminder_view, name="reminder"),
    path("ATriggerVerify.txt",file),
    path("auth/", auth, name='get_secret'),
    path("menu/", menu, name='menu'),
    path("upload", upload, name="upload")

]
