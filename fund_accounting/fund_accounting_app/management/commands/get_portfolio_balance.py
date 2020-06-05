# from fund_accounting_app.models import
import fund_accounting_app.operations.get_portfolio_balance as default
from django.core.management.base import BaseCommand, CommandError
import datetime


def valid_date(s):
    if not s:
        return None
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise CommandError(msg)


class Command(BaseCommand):

    help = "Get Porfolio Balance ."

    def add_arguments(self, parser):
        # parser.add_argument("name", type=str, help="Name of this portfolio")
        parser.add_argument("pf_number", type=int, help="Number of porfolio")
        parser.add_argument("date", type=valid_date, help="Date for balance")

    def handle(self, *args, **options):

        NAV = default.get_top_level_portfolio_balance(
            options["pf_number"], options["date"]
        )

        self.stdout.write(self.style.SUCCESS("NAV (unrealized) is"))
