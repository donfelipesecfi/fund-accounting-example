# def
from hordak.models import Transaction, Leg
from fund_accounting_app.models import Deal


def get_last_booking_date_interest(deal: Deal):

    all_transactions = Leg.objects.filter(account=deal.fi_account_value).all()
    last_transaction = (
        Transaction.objects.filter(legs__in=all_transactions).order_by("-date").first()
    )
    if last_transaction:
        return last_transaction.date
    all_transactions = Leg.objects.filter(account=deal.fi_account_stock).all()
    last_transaction = (
        Transaction.objects.filter(legs__in=all_transactions).order_by("-date").first()
    )
    return last_transaction.date
