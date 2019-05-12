from django.contrib.auth.management.commands import createsuperuser

from infusionset_reminder.settings import SECRET_KEY, app_name


class Command(createsuperuser.Command):
    """
    command for creating custom superuser
    """

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("creating admin ..."))

        options.setdefault('interactive', False)
        database = options.get('database')
        user_data = {
            'username': SECRET_KEY,
            'password': app_name,
            'email': "",
        }
        self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)

        if options.get('verbosity', 0) >= 1:
            self.stdout.write("Superuser created successfully.")
