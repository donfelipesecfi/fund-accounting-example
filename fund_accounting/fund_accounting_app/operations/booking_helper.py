# def
from hordak.models import Transaction, Leg


def get_last_booking_date(account):

    all_transactions = Leg.objects.filter(account=account).all()
    last_transaction = (
        Transaction.objects.filter(legs__in=all_transactions).order_by("-date").first()
    )

    # date = Leg.objects.filter(account=account,transaction__).all()
    return last_transaction.date
