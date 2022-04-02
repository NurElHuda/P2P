from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.utils.crypto import get_random_string

from app_src.api.models import Admin, User


class Command(createsuperuser.Command):
    help = "Create new admin."

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument("--password", dest="password", default=None)

    def handle(self, *args, **options):
        password = options.get("password")
        username = get_random_string(length=12)
        email = options.get("email")

        if not password or not email:
            raise CommandError("--email and --password are required")

        data = {"username": username, "password": password, "email": email}
        user = User.objects.create_superuser(**data)
        user.is_admin = True
        user.save()

        admin = Admin.objects.create(user=user)
