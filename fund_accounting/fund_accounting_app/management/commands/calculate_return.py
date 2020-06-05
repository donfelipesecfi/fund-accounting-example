# from fund_accounting_app.models import
import fund_accounting_app.operations.get_portfolio_balance as default
from django.core.management.base import BaseCommand, CommandError
import datetime
import pandas


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

        parser.add_argument("pf_number", type=int, help="Number of porfolio")
        parser.add_argument(
            "start_date", type=valid_date, help="Start date of reference period"
        )
        parser.add_argument(
            "end_date", type=valid_date, help="End date of reference period"
        )

    def handle(self, *args, **options):

        NAVs = default.get_top_level_portfolio_returns(
            options["pf_number"], options["start_date"], options["end_date"]
        )
        relative = {}
        absolute = {}
        for key in NAVs.keys():

            relative[key] = NAVs[key]["relative"]
            absolute[key] = NAVs[key]["absolute"]

        pd_relative = pandas.DataFrame().from_dict(relative)

        pd_absolute = pandas.DataFrame.from_dict(
            {
                (i, j): absolute[i][j]
                for i in absolute.keys()
                for j in absolute[i].keys()
            },
            orient="index",
        )

        pd_absolute.to_csv(
            f'PF-Development-Absolute-Vals_{options["start_date"].strftime("%d-%m-%Y")}_{options["end_date"].strftime("%d-%m-%Y")}.csv'
        )

        pd_relative.to_csv(
            f'Returns_{options["start_date"].strftime("%d-%m-%Y")}_{options["end_date"].strftime("%d-%m-%Y")}.csv'
        )

        self.stdout.write(self.style.SUCCESS(f"{NAVs}"))
