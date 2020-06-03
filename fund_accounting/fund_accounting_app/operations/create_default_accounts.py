from hordak.models import Account, Leg, Transaction, Money
from fund_accounting_app.models import FundManager
import uuid
from decimal import Decimal
from django.db import transaction as db_transaction


def create_parent_accounts():

    portfolio_1_account = Account(
        name="Portfolio", code="001", type=Account.TYPES.equity, currencies=["USD"],
    ).save()
    usd_cash_account = Account(
        name="USD Account",
        code="002",
        type=Account.TYPES.asset,
        is_bank_account=True,
        currencies=["USD"],
    ).save()
    equity_account = Account(
        name="Equity", code="003", type=Account.TYPES.asset, currencies=["USD"],
    ).save()
    fixed_income_account = Account(
        name="Fixed Income", code="004", type=Account.TYPES.asset, currencies=["USD"],
    ).save()
    equity_account_unrealized = Account(
        name="Equity unrealized",
        code="005",
        type=Account.TYPES.liability,
        currencies=["USD"],
    ).save()
    fixed_income_account_unrealized = Account(
        name="Fixed Income unrealized",
        code="006",
        type=Account.TYPES.liability,
        currencies=["USD"],
    ).save()


def get_parent(code):
    return Account.objects.get(code=code)


def create_portfolio(pf_name, pf_number):

    portfolio_1_account = Account(
        name=f"Portfolio {pf_name} ",
        parent=get_parent("001"),
        code=f"{pf_number}01",
        full_code=f"001_{pf_number}",
        currencies=["USD"],
    ).save()

    usd_cash_account = Account(
        name=f"USD Account {pf_name} ",
        parent=get_parent("002"),
        code=f"{pf_number}02",
        full_code=f"002_{pf_number}",
        currencies=["USD"],
    ).save()

    equity_account = Account(
        name=f"Equity {pf_name} ",
        code=f"{pf_number}03",
        parent=get_parent("003"),
        full_code=f"003_{pf_number}",
        currencies=["USD"],
    ).save()

    fixed_income_account = Account(
        name=f"Fixed Income  {pf_name} ",
        parent=get_parent("004"),
        code=f"{pf_number}04",
        full_code=f"004_{pf_number}",
        currencies=["USD"],
    ).save()
    equity_account_unrealized = Account(
        name=f"Equity unrealized {pf_name} ",
        parent=get_parent("005"),
        code=f"{pf_number}05",
        full_code=f"005_{pf_number}",
        currencies=["USD"],
    ).save()
    fixed_income_account_unrealized = Account(
        name=f"Fixed Income unrealized {pf_name} ",
        parent=get_parent("006"),
        code=f"{pf_number}06",
        full_code=f"006_{pf_number}",
        currencies=["USD"],
    ).save()


def add_fund_manager_add_book_cash(
    pf_number, fund_manager, amount,
):
    import pdb

    pdb.set_trace()
    account = Account(
        name=f"Fund Manager {fund_manager}",
        parent=get_parent(f"{pf_number}01"),
        code="111",
        full_code=f"001_{pf_number}_001",
        currencies=["USD"],
    )
    account.save()

    cash_account = Account(
        name=f"USD Account {fund_manager}",
        parent=get_parent(f"{pf_number}02"),
        code=f"{pf_number}12",
        full_code=f"002_{pf_number}_001",
        currencies=["USD"],
    )
    cash_account.save()

    manager = FundManager(
        name=fund_manager,
        account=get_parent(f"{pf_number}01"),
        fund=uuid.uuid4(),
        hurdle=Decimal(0.1),
    ).save()

    with db_transaction.atomic():

        transaction = Transaction.objects.create()
        Leg.objects.create(
            transaction=transaction, account=cash_account, amount=Money(amount, "USD")
        )
        Leg.objects.create(
            transaction=transaction, account=account, amount=Money(amount * -1, "USD")
        )
