from fund_accounting_app.models import Deal
from .booking_helper import get_last_booking_date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
from datequarter import DateQuarter
from django.db import transaction as db_transaction

from hordak.models import Transaction, Leg, Money
from hordak.utilities.currency import Balance


import datetime


def calculate_interest_in_quarter(amount, interest):
    if isinstance(amount, Balance):
        import pdb

        pdb.set_trace()
        amount = amount.__getitem__("USD")
    return amount * (1 + (interest / 4)) - amount


def book_interest_unrealized(deal: Deal, amount: Money, date):
    import pdb

    pdb.set_trace()
    with db_transaction.atomic():

        transaction = Transaction.objects.create(date=date)
        Leg.objects.create(
            transaction=transaction, account=deal.fi_account, amount=amount * -1,
        )
        Leg.objects.create(
            transaction=transaction, account=deal.fi_unrealized_account, amount=amount,
        )


def book_interest_all_deals_from_last_booking_day():

    all_deals = Deal.objects.all()

    for deal in all_deals:
        last_booking_day = get_last_booking_date(deal.fi_account)
        difference_in_quarters = DateQuarter.from_date(
            datetime.datetime.now()
        ) - DateQuarter.from_date(last_booking_day)

        for quarter in range(difference_in_quarters):
            last_day_in_quarter = [
                day for day in DateQuarter.from_date(last_booking_day).days()
            ][-1]
            interest = calculate_interest_in_quarter(
                deal.fi_account.balance(as_of=last_day_in_quarter), deal.interest_loan
            )
            book_interest_unrealized(deal, interest, last_day_in_quarter)
            last_booking_day = last_day_in_quarter + relativedelta(months=+3)
