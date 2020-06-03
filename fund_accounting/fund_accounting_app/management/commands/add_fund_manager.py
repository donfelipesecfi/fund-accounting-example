# from fund_accounting_app.models import
import fund_accounting_app.operations.create_default_accounts as default
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = "Add new fund manager and book the cash."

    def add_arguments(self, parser):

        parser.add_argument("pf_number", type=int, help="Number of portfolio")
        parser.add_argument("name", type=str, help="Name of this fund manager")
        parser.add_argument("amount", type=float, help="USD Amount of Fund Manager")

    def handle(self, *args, **options):

        default.add_fund_manager_add_book_cash(
            options["pf_number"], options["name"], options["amount"]
        )

        self.stdout.write(
            self.style.SUCCESS("Successfully added fund manager and booked cash")
        )
