from django.core.management.base import BaseCommand
import requests
from infusionset_reminder.settings import SECRET_KEY


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("waking up ..."))
        requests.get("https://reminder-rekina.herokuapp.com/get/?key={0}".format(SECRET_KEY))
        self.stdout.write(self.style.SUCCESS("website successfully woke up"))
