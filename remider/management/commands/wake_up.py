import requests
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from django.conf import settings


class Command(BaseCommand):
    """
    command for triggering our site
    """

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO(_("waking up ...")))
        requests.get("https://{1}.herokuapp.com/reminder/?key={0}".format(settings.SECRET_KEY, settings.APP_NAME))
        self.stdout.write(self.style.SUCCESS(_("website successfully woke up")))
