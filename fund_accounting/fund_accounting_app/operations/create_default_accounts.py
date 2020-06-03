from hordak.models import Account, Leg, Transaction, Money
from fund_accounting_app.models import FundManager, Deal
import uuid
from decimal import Decimal
from django.db import transaction as db_transaction


def create_parent_accounts():
    """
    
    Function to create all root-accounts needed.


    """
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
    pf_number, fund_manager, amount, date=FileNotFoundError
):

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
    )
    manager.save()

    with db_transaction.atomic():
        if date:
            transaction = Transaction.objects.create(date=date)
        else:
            transaction = Transaction.objects.create()

        Leg.objects.create(
            transaction=transaction, account=cash_account, amount=Money(amount, "USD"),
        )
        Leg.objects.create(
            transaction=transaction, account=account, amount=Money(amount * -1, "USD"),
        )


def add_deal_accounts(
    company_name,
    fund_manager,
    company,
    total_loan_amount,
    total_collateral_shares,
    interest_loan,
    interest_equity,
) -> Deal:

    fund_manager = FundManager.objects.get(id=fund_manager)
    import pdb

    pdb.set_trace()
    account_equity = Account(
        name=f"Equity {company_name}",
        code=None,
        full_code=None,
        parent=get_parent(f"{fund_manager.fund_number}03"),
        currencies=["USD"],
    )
    account_equity.save()

    account_equity_unreal = Account(
        name=f"Unrealized Equity {company_name}",
        code=None,
        full_code=None,
        parent=get_parent(f"{fund_manager.fund_number}05"),
        currencies=["USD"],
    )
    account_equity_unreal.save()

    account_fixed_income = Account(
        name=f"Fixed Income {company_name}",
        code=None,
        full_code=None,
        parent=get_parent(f"{fund_manager.fund_number}04"),
        currencies=["USD"],
    )
    account_fixed_income.save()

    account_fixed_income_unreal = Account(
        name=f"Unrealized Fixed Income {company_name}",
        code=None,
        full_code=None,
        parent=get_parent(f"{fund_manager.fund_number}06"),
        currencies=["USD"],
    )
    account_fixed_income_unreal.save()

    deal = Deal(
        company=company,
        fund_manager=fund_manager,
        eq_account=account_equity,
        eq_unrealized_account=account_equity_unreal,
        fi_account=account_fixed_income,
        fi_unrealized_account=account_fixed_income_unreal,
        total_loan_amount=total_loan_amount,
        total_collateral_shares=total_collateral_shares,
        interest_loan=interest_loan,
        interest_equity=interest_equity,
    )

    deal.save()

    return deal


def book_deal_values(
    deal: Deal, price_valuation: Decimal, initial_booking=False, date=None
):

    if initial_booking:

        cash_account = Account.objects.get(code=f"{deal.fund_manager.fund_number}02")
        cash_account.transfer_to(
            to_account=deal.fi_account, amount=Money(deal.total_loan_amount, "USD")
        )
        with db_transaction.atomic():
            if date:
                transaction = Transaction.objects.create(date=date)
            else:
                transaction = Transaction.objects.create()
            transaction_value = deal.portfolio_equity * price_valuation
            Leg.objects.create(
                transaction=transaction,
                account=deal.eq_account,
                amount=Money(transaction_value, "USD"),
            )
            Leg.objects.create(
                transaction=transaction,
                account=deal.eq_unrealized_account,
                amount=Money(transaction_value * -1, "USD"),
            )

    else:

        raise Exception("Not Implemented")


def initial_book_deal(
    deal_date,
    company_name,
    fund_manager,
    company,
    total_loan_amount,
    total_collateral_shares,
    interest_loan,
    interest_equity,
    value_per_share,
):
    import pdb

    pdb.set_trace()
    deal = add_deal_accounts(
        company_name,
        fund_manager,
        company,
        total_loan_amount,
        total_collateral_shares,
        interest_loan,
        interest_equity,
    )
    book_deal_values(
        deal=deal, price_valuation=value_per_share, date=deal_date, initial_booking=True
    )
