from fund_accounting_app.models import FundManager, Deal
from hordak.models import Account, Transaction, Leg
from hordak.utilities.currency import Money
from .helpers import get_account_code, get_parent, get_deal_id
from decimal import Decimal
from django.db import transaction as db_transaction


def add_deal_accounts(
    deal_date,
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
        date=deal_date,
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

        deal.last_booking_equity_valuation = date
        deal.save(update_fields=["last_booking_equity_valuation"])

    else:

        raise Exception("Not Implemented")


def book_deal(
    date,
    company_name,
    fund_manager,
    company,
    total_loan_amount,
    total_collateral_shares,
    interest_loan,
    interest_equity,
    value_per_share,
    **kwargs,
):

    deal = add_deal_accounts(
        date,
        company_name,
        fund_manager,
        company,
        total_loan_amount,st
        total_collateral_shares,
        interest_loan,
        interest_equity,
    )

    book_deal_values(
        deal=deal, price_valuation=value_per_share, date=deal_date, initial_booking=True
    )

    return deal
