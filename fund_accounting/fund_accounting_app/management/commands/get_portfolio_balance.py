# from fund_accounting_app.models import
import fund_accounting_app.operations.get_portfolio_balance as default
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = "Get Porfolio Balance ."

    def add_arguments(self, parser):
        # parser.add_argument("name", type=str, help="Name of this portfolio")
        parser.add_argument("pf_number", type=int, help="Name of this portfolio")

    def handle(self, *args, **options):
        import pdb

        pdb.set_trace()
        default.get_top_level_portfolio_balance(options["pf_number"])

        self.stdout.write(self.style.SUCCESS("Successfully added parent accounts"))
