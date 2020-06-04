from hordak.models import Account, Money
from .helper_conversions import convert_balance_to_money_usd


def get_sub_portfolio_value(code_asset, code_liab=None, **kwargs):
    amount = convert_balance_to_money_usd(
        Account.objects.get(code=code_asset).balance(**kwargs)
    )
    amount_unrealized = Money(0, "USD")
    if code_liab:
        amount_unrealized = convert_balance_to_money_usd(
            Account.objects.get(code=code_liab).balance(**kwargs)
        )

    return {
        "NAV (unrealized)": amount,
        "NAV (realized)": amount - amount_unrealized,
    }


def get_top_level_portfolio_value(pf_number, date=None):
    kwargs = {}
    if date:
        kwargs = {"as_of": date}

    NAV_Equity = get_sub_portfolio_value(f"C{pf_number}", f"E{pf_number}", **kwargs)

    NAV_CASH = get_sub_portfolio_value(f"B{pf_number}", **kwargs)

    NAV_FI = get_sub_portfolio_value(f"D{pf_number}", f"F{pf_number}", **kwargs)

    import pdb

    pdb.set_trace()

    return NAV_Equity
