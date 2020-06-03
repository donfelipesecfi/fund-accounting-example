# from fund_accounting_app.models import
import fund_accounting_app.operations.create_default_accounts as default
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = "Inititate a complete new portfolio."

    def add_arguments(self, parser):
        parser.add_argument("name", type=int, help="Name of this portfolio")

    def handle(self, *args, **options):

        default.create_parent_accounts()

        self.stdout.write(self.style.SUCCESS("Successfully added parent accounts"))
