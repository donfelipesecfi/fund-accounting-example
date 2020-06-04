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
        pddf = pandas.DataFrame.from_dict(
            {(i, j): NAVs[i][j] for i in NAVs.keys() for j in NAVs[i].keys()},
            orient="index",
        )
        import pdb

        pdb.set_trace()
        pddf.to_csv(
            f'Returns_{options["start_date"].strftime("%d-%m-%Y")}_{options["end_date"].strftime("%d-%m-%Y")}.csv'
        )

        self.stdout.write(self.style.SUCCESS(f"{NAVs}"))
