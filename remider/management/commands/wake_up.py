import requests
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _

from infusionset_reminder.settings import SECRET_KEY, app_name


class Command(BaseCommand):
    """
    command for triggering our site
    """

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO(_("waking up ...")))
        requests.get("https://{1}.herokuapp.com/reminder/?key={0}".format(SECRET_KEY, app_name))
        self.stdout.write(self.style.SUCCESS(_("website successfully woke up")))
