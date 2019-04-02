from django.urls import path

from .views import get_from_api, calculate, notify, home
urlpatterns = [
    path("", home),
    path("get/", get_from_api, name="get"),
    path("calculate/", calculate, name="calculate"),
    path("notify/", notify, name="notify"),
]
