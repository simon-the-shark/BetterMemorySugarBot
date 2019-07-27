from django.contrib.auth.management.commands import createsuperuser
from django.utils.translation import ugettext as _

from django.conf import settings


class Command(createsuperuser.Command):
    """
    command for creating custom superuser
    """

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO(_("creating admin ...")))

        options.setdefault('interactive', False)
        database = options.get('database')
        user_data = {
            'username': settings.APP_NAME,
            'password': settings.SECRET_KEY,
            'email': "",
        }
        self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)

        if options.get('verbosity', 0) >= 1:
            self.stdout.write(_("Superuser created successfully."))
