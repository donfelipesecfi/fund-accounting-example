from hordak.models import Account, Money
from .helper_conversions import convert_balance_to_money_usd
import decimal


def get_equity_portfolio_value(pf_number, **kwargs):

    return (
        Account.objects.get(code=f"C{pf_number}").balance(**kwargs).__getitem__("USD")
    )


def get_equity_stock_portfolio_value(pf_number, **kwargs):

    return (
        Account.objects.get(code=f"E{pf_number}").balance(**kwargs).__getitem__("USD")
    )


def get_equity_value_portfolio_value(pf_number, **kwargs):

    return (
        Account.objects.get(code=f"D{pf_number}").balance(**kwargs).__getitem__("USD")
    )


def get_fixed_income_portfolio_value(pf_number, **kwargs):

    return (
        Account.objects.get(code=f"F{pf_number}").balance(**kwargs).__getitem__("USD")
    )


def get_fixed_income_stock_portfolio_value(pf_number, **kwargs):

    return (
        Account.objects.get(code=f"H{pf_number}").balance(**kwargs).__getitem__("USD")
    )


def get_fixed_income_value_portfolio_value(pf_number, **kwargs):

    return (
        Account.objects.get(code=f"G{pf_number}").balance(**kwargs).__getitem__("USD")
    )


def get_top_level_portfolio_value(pf_number, date=None):
    kwargs = {}
    if date:
        kwargs = {"as_of": date}

    NAV_equity = get_equity_portfolio_value(pf_number, **kwargs)
    NAV_equity_stock = get_equity_stock_portfolio_value(pf_number, **kwargs)
    NAV_equity_value = get_equity_value_portfolio_value(pf_number, **kwargs)

    NAV_fixed_income = get_fixed_income_portfolio_value(pf_number, **kwargs)
    NAV_fixed_income_stock = get_fixed_income_stock_portfolio_value(pf_number, **kwargs)
    NAV_fixed_income_value = get_fixed_income_value_portfolio_value(pf_number, **kwargs)

    NAV_cash = (
        Account.objects.get(code=f"B{pf_number}").balance(**kwargs).__getitem__("USD")
    )

    return {
        "total": {
            "total_value": NAV_equity + NAV_fixed_income + NAV_cash,
            "change_value": NAV_equity_value + NAV_fixed_income_value,
            "added_value": NAV_equity_stock + NAV_fixed_income_stock,
        },
        "equity": {
            "total_value": NAV_equity,
            "change_value": NAV_equity_value,
            "added_value": NAV_equity_stock,
        },
        "fixed_income": {
            "total_value": NAV_fixed_income,
            "change_value": NAV_fixed_income_value,
            "added_value": NAV_fixed_income_stock,
        },
        "cash": {"total_value": NAV_cash},
    }


def calulate_return(val_t0, val_t1):

    return_value = None
    try:
        return_value = (val_t1 / val_t0) - 1
    except decimal.InvalidOperation:
        pass
    except decimal.ZeroDivisionError:
        pass
    return return_value


def get_top_level_portfolio_returns(pf_number, ref_date_start, ref_date_end):

    portfolio_ref_date_start = get_top_level_portfolio_value(pf_number, ref_date_start)
    portfolio_ref_date_end = get_top_level_portfolio_value(pf_number, ref_date_end)
    return_dict = {}

    import pdb

    pdb.set_trace()

    for key in portfolio_ref_date_start.keys():
        inner_dict = {}
        relative_vals = {}
        absolute_vals = {}
        for key2 in portfolio_ref_date_start[key].keys():
            relative_vals[f"{key2} in %"] = calulate_return(
                portfolio_ref_date_start[key][key2], portfolio_ref_date_end[key][key2]
            )

            absolute_vals[key2] = {
                "begin_period": portfolio_ref_date_start[key][key2],
                "end_period": portfolio_ref_date_end[key][key2],
            }
        reative_absolut_values = {"relative": relative_vals, "absolute": absolute_vals}
        return_dict[key] = reative_absolut_values

    return return_dict
