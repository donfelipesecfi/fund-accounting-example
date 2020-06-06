from hordak.utilities.currency import Balance
from hordak.models import Account
from fund_accounting_app.models import Deal


def convert_balance_to_money_usd(balance: Balance):
    return balance.__getitem__("USD")


def get_parent(code):
    return Account.objects.get(code=code)


def get_account_code():
    return Account.objects.all().count() + 1


def get_deal_id():
    return Deal.objects.all().count() + 1
