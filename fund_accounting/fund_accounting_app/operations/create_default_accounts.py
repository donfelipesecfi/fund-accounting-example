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
        name="Portfolio", code="A", type=Account.TYPES.equity, currencies=["USD"],
    ).save()
    usd_cash_account = Account(
        name="USD Account",
        code="B",
        type=Account.TYPES.asset,
        is_bank_account=True,
        currencies=["USD"],
    ).save()
    equity_account = Account(
        name="Equity", code="C", type=Account.TYPES.asset, currencies=["USD"],
    ).save()
    fixed_income_account = Account(
        name="Fixed Income", code="F", type=Account.TYPES.asset, currencies=["USD"],
    ).save()
    equity_account_unrealized = Account(
        name="Equity unrealized",
        code="I",
        type=Account.TYPES.liability,
        currencies=["USD"],
    ).save()
    fixed_income_account_unrealized = Account(
        name="Fixed Income unrealized",
        code="J",
        type=Account.TYPES.liability,
        currencies=["USD"],
    ).save()


def get_parent(code):
    return Account.objects.get(code=code)


def get_account_code():
    return Account.objects.all().count() + 1


def create_portfolio(pf_name, pf_number):

    import pdb

    pdb.set_trace()

    portfolio_1_account = Account(
        name=f"Portfolio {pf_name} ",
        parent=get_parent("A"),
        code=f"A{pf_number}",
        full_code=f"A_{pf_number}",
        currencies=["USD"],
    ).save()

    usd_cash_account = Account(
        name=f"USD Account {pf_name} ",
        parent=get_parent("B"),
        code=f"B{pf_number}",
        full_code=f"B_{pf_number}",
        currencies=["USD"],
    ).save()

    equity_account = Account(
        name=f"Equity {pf_name} ",
        code=f"C{pf_number}",
        parent=get_parent("C"),
        full_code=f"C_{pf_number}",
        currencies=["USD"],
    ).save()

    equity_account_value = Account(
        name=f"Equity Value {pf_name} ",
        code=f"D{pf_number}",
        parent=get_parent(f"C{pf_number}"),
        full_code=f"D_{pf_number}",
        currencies=["USD"],
    ).save()

    equity_account_stock = Account(
        name=f"Equity Stock {pf_name} ",
        code=f"E{pf_number}",
        parent=get_parent(f"C{pf_number}"),
        full_code=f"E_{pf_number}",
        currencies=["USD"],
    ).save()

    fixed_income_account = Account(
        name=f"Fixed Income  {pf_name} ",
        parent=get_parent("F"),
        code=f"F{pf_number}",
        full_code=f"F_{pf_number}",
        currencies=["USD"],
    ).save()

    fixed_income_account_value = Account(
        name=f"Fixed Income Value {pf_name} ",
        parent=get_parent(f"F{pf_number}"),
        code=f"G{pf_number}",
        full_code=f"G_{pf_number}",
        currencies=["USD"],
    ).save()

    fixed_income_account_stock = Account(
        name=f"Fixed Income Stock {pf_name} ",
        parent=get_parent(f"F{pf_number}"),
        code=f"H{pf_number}",
        full_code=f"H_{pf_number}",
        currencies=["USD"],
    ).save()

    equity_account_unrealized = Account(
        name=f"Equity unrealized {pf_name} ",
        parent=get_parent("I"),
        code=f"I{pf_number}",
        full_code=f"I_{pf_number}",
        currencies=["USD"],
    ).save()

    fixed_income_account_unrealized = Account(
        name=f"Fixed Income unrealized {pf_name} ",
        parent=get_parent("J"),
        code=f"J{pf_number}",
        full_code=f"J{pf_number}",
        currencies=["USD"],
    ).save()


def add_fund_manager_add_book_cash(pf_number, fund_manager, amount, date=None):

    code_manager = get_account_code()
    account = Account(
        name=f"Fund Manager {fund_manager}",
        parent=get_parent(f"A{pf_number}"),
        code=code_manager,
        full_code=f"A_{pf_number}_{code_manager}",
        currencies=["USD"],
    )
    account.save()

    cash_account = Account(
        name=f"USD Account {fund_manager}",
        parent=get_parent(f"B{pf_number}"),
        code=f"{get_account_code()}",
        full_code=f"B_{pf_number}_{get_account_code()}",
        currencies=["USD"],
    )
    cash_account.save()

    manager = FundManager(
        name=fund_manager,
        account=get_parent(code_manager),
        fund=uuid.uuid4(),
        fund_number=pf_number,
        hurdle=Decimal(0.1),
    )
    manager.save()

    with db_transaction.atomic():
        if date:
            transaction = Transaction.objects.create(date=date)
        else:
            transaction = Transaction.objects.create()

        Leg.objects.create(
            transaction=transaction,
            account=cash_account,
            amount=Money(amount * -1, "USD"),
        )
        Leg.objects.create(
            transaction=transaction, account=account, amount=Money(amount, "USD"),
        )


def get_deal_id():

    return Deal.objects.all().count() + 1


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

    account_equity_stock = Account(
        name=f"Equity Stock {company_name}",
        code=get_account_code(),
        full_code=f"D_{fund_manager.fund_number}_{get_deal_id()}",
        parent=get_parent(f"D{fund_manager.fund_number}"),
        currencies=["USD"],
    )
    account_equity_stock.save()

    account_equity_value = Account(
        name=f"Equity Value {company_name}",
        code=get_account_code(),
        full_code=f"E_{fund_manager.fund_number}_{get_deal_id()}",
        parent=get_parent(f"E{fund_manager.fund_number}"),
        currencies=["USD"],
    )
    account_equity_value.save()

    account_equity_unreal = Account(
        name=f"Unrealized Equity {company_name}",
        code=get_account_code(),
        full_code=f"I_{fund_manager.fund_number}_{get_deal_id()}",
        parent=get_parent(f"I{fund_manager.fund_number}"),
        currencies=["USD"],
    )
    account_equity_unreal.save()

    account_fixed_income_value = Account(
        name=f"Fixed Income Value {company_name}",
        code=get_account_code(),
        full_code=f"G_{fund_manager.fund_number}_{get_deal_id()}",
        parent=get_parent(f"G{fund_manager.fund_number}"),
        currencies=["USD"],
    )
    account_fixed_income_value.save()

    account_fixed_income_stock = Account(
        name=f"Fixed Income Stock {company_name}",
        code=get_account_code(),
        full_code=f"H_{fund_manager.fund_number}_{get_deal_id()}",
        parent=get_parent(f"H{fund_manager.fund_number}"),
        currencies=["USD"],
    )
    account_fixed_income_stock.save()

    account_fixed_income_unreal = Account(
        name=f"Unrealized Fixed Income {company_name}",
        code=get_account_code(),
        full_code=f"J_{fund_manager.fund_number}_{get_deal_id()}",
        parent=get_parent(f"J{fund_manager.fund_number}"),
        currencies=["USD"],
    )
    account_fixed_income_unreal.save()

    deal = Deal(
        company=company,
        fund_manager=fund_manager,
        eq_account_value=account_equity_value,
        eq_account_stock=account_equity_stock,
        eq_unrealized_account=account_equity_unreal,
        fi_account_value=account_fixed_income_value,
        fi_account_stock=account_fixed_income_stock,
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

        cash_account = Account.objects.get(code=f"B{deal.fund_manager.fund_number}")
        cash_account.transfer_to(
            to_account=deal.fi_account_stock,
            date=date if date is not None else None,
            amount=Money(deal.total_loan_amount, "USD",),
        )
        with db_transaction.atomic():
            if date:
                transaction = Transaction.objects.create(date=date)
            else:
                transaction = Transaction.objects.create()
            transaction_value = deal.portfolio_equity * price_valuation
            Leg.objects.create(
                transaction=transaction,
                account=deal.eq_account_value,
                amount=Money(transaction_value * -1, "USD"),
            )
            Leg.objects.create(
                transaction=transaction,
                account=deal.eq_unrealized_account,
                amount=Money(transaction_value, "USD"),
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
