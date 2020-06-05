# from fund_accounting_app.models import
import fund_accounting_app.operations.create_default_accounts as default
from django.core.management.base import BaseCommand, CommandError
import datetime
import uuid


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise CommandError(msg)


class Command(BaseCommand):

    help = "Add Deal"

    def add_arguments(self, parser):

        parser.add_argument(
            "deal_date", type=valid_date, help="Date on which we add this to PF"
        )
        parser.add_argument("fund_manager_id", type=int)
        parser.add_argument("total_loan_amount", type=int)
        parser.add_argument("total_collateral_shares", type=int)
        parser.add_argument("interest_loan", type=float)
        parser.add_argument("interest_equity", type=float)
        parser.add_argument("value_per_share", type=float)

    def handle(self, *args, **options):

        default.initial_book_deal(
            deal_date=options["deal_date"],
            company_name="TEST COMP",
            fund_manager=options["fund_manager_id"],
            company=uuid.uuid4(),
            total_loan_amount=options["total_loan_amount"],
            total_collateral_shares=options["total_collateral_shares"],
            interest_loan=options["interest_loan"],
            interest_equity=options["interest_equity"],
            value_per_share=options["value_per_share"],
        )

        self.stdout.write(self.style.SUCCESS("Successfully added parent accounts"))
