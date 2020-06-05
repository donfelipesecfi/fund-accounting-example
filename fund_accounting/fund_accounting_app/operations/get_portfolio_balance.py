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

    total_nav = NAV_equity + NAV_fixed_income + NAV_cash

    return {
        "total": {
            "total_value": {"value": total_nav, "weight": 1},
            "change_value": {
                "value": NAV_equity_value + NAV_fixed_income_value,
                "weight": (NAV_equity_value + NAV_fixed_income_value) / total_nav,
            },
            "added_value": {
                "value": NAV_equity_stock + NAV_fixed_income_stock,
                "weight": (NAV_equity_stock + NAV_fixed_income_stock) / total_nav,
            },
            "uninvested_cash": {"value": NAV_cash, "weight": (NAV_cash / total_nav)},
        },
        "equity": {
            "total_value": {"value": NAV_equity, "weight": (NAV_equity / total_nav),},
            "change_value": {
                "value": NAV_equity_value,
                "weight": NAV_equity_value / NAV_equity,
            },
            "added_value": {
                "value": NAV_equity_stock,
                "weight": (NAV_equity_stock / NAV_equity),
            },
        },
        "fixed_income": {
            "total_value": {
                "value": NAV_fixed_income,
                "weight": (NAV_fixed_income / total_nav),
            },
            "change_value": {
                "value": NAV_fixed_income_value,
                "weight": (NAV_fixed_income_value / NAV_fixed_income),
            },
            "added_value": {
                "value": NAV_fixed_income_stock,
                "weight": (NAV_fixed_income_stock / NAV_fixed_income),
            },
        },
        "cash": {"total_value": {"value": NAV_cash, "weight": (NAV_cash / total_nav)}},
    }


def calulate_return(val_t0, val_t1, weight=1):

    return_value = None
    try:
        return_value = weight * (val_t1 / val_t0)
    except decimal.InvalidOperation:
        pass
    except decimal.ZeroDivisionError:
        pass
    if weight == 1:
        return_value = return_value - 1

    return return_value


def get_top_level_portfolio_returns(pf_number, ref_date_start, ref_date_end):

    portfolio_ref_date_start = get_top_level_portfolio_value(pf_number, ref_date_start)
    portfolio_ref_date_end = get_top_level_portfolio_value(pf_number, ref_date_end)
    return_dict = {}
    for key in portfolio_ref_date_start.keys():

        relative_vals = {}
        absolute_vals = {}
        for key2 in portfolio_ref_date_start[key].keys():

            relative_vals[f"{key2} in %"] = calulate_return(
                portfolio_ref_date_start[key][key2]["value"],
                portfolio_ref_date_end[key][key2]["value"],
                weight=portfolio_ref_date_end[key][key2]["weight"],
            )

            absolute_vals[key2] = {
                "begin_period": portfolio_ref_date_start[key][key2]["value"],
                "end_period": portfolio_ref_date_end[key][key2]["value"],
            }
        reative_absolut_values = {"relative": relative_vals, "absolute": absolute_vals}
        return_dict[key] = reative_absolut_values

    return return_dict
