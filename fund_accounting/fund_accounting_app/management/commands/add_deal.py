# from fund_accounting_app.models import
import fund_accounting_app.operations.create_default_accounts as default
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = "Add Deal"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Name of this portfolio")
        parser.add_argument("pf_number", type=str, help="Name of this portfolio")

    def handle(self, *args, **options):

        default.create_portfolio(options["name"], options["pf_number"])

        self.stdout.write(self.style.SUCCESS("Successfully added parent accounts"))
