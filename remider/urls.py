from django.urls import path
from django.conf.urls import url
from django.views.generic import RedirectView

from .views import get_from_api, calculate, notify, home

urlpatterns = [
    path("", home),
    path("get/", get_from_api, name="get"),
    path("calculate/", calculate, name="calculate"),
    path("notify/<int:idays>/<int:ihours>/<int:sdays>/<int:shours>/<int:imicroseconds>/<int:smicroseconds>/", notify,
         name="notify"),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
]
