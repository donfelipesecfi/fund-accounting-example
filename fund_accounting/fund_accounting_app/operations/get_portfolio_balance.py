from hordak.models import Account, Money
from .helper_conversions import convert_balance_to_money_usd
import decimal


def calculate_value_fixed_income_from_deal(deal, **kwargs):

    return deal.fi_account_value.balance(**kwargs).__getitem__("USD")


def calculate_stock_fixed_income_from_deal(deal, **kwargs):

    return deal.fi_account_stock.balance(**kwargs).__getitem__("USD")


def calculate_total_value_fixed_income_from_deal(deal, **kwargs):

    stock = calculate_stock_fixed_income_from_deal(deal, **kwargs)
    value = calculate_value_fixed_income_from_deal(deal, **kwargs)

    return stock + value


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
        },
        "equity": {
            "total_value": {"value": NAV_equity, "weight": (NAV_equity / total_nav),},
            "change_value": {
                "value": NAV_equity_value,
                "weight": NAV_equity_value / total_nav,
            },
            "added_value": {
                "value": NAV_equity_stock,
                "weight": (NAV_equity_stock / total_nav),
            },
        },
        "fixed_income": {
            "total_value": {
                "value": NAV_fixed_income,
                "weight": (NAV_fixed_income / total_nav),
            },
            "change_value": {
                "value": NAV_fixed_income_value,
                "weight": (NAV_fixed_income_value / total_nav),
            },
            "added_value": {
                "value": NAV_fixed_income_stock,
                "weight": (NAV_fixed_income_stock / total_nav),
            },
        },
        "cash": {"total_value": {"value": NAV_cash, "weight": 1}},
    }


def calulate_return(val_t0, val_t1):

    return_value = None
    try:
        return_value = (val_t1 / val_t0) - 1
    except decimal.InvalidOperation:
        pass
    except decimal.DivisionByZero:
        pass

    return return_value


def get_top_level_portfolio_returns(pf_number, ref_date_start, ref_date_end):

    portfolio_ref_date_start = get_top_level_portfolio_value(pf_number, ref_date_start)
    portfolio_ref_date_end = get_top_level_portfolio_value(pf_number, ref_date_end)

    portfolio_ref_date_start

    return_dict = {}
    for key in portfolio_ref_date_start.keys():

        relative_vals = {}
        absolute_vals = {}
        for key2 in portfolio_ref_date_start[key].keys():

            if key2 == "total_value":
                relative_vals[f"{key2} in %"] = calulate_return(
                    portfolio_ref_date_start[key][key2]["value"],
                    portfolio_ref_date_end[key][key2]["value"],
                )
                weight = 1
                if not key == "total":
                    weight = (
                        portfolio_ref_date_end[key][key2]["value"]
                        / portfolio_ref_date_end["total"]["total_value"]["value"]
                    )

                relative_vals[f"weight"] = weight

            absolute_vals[key2] = {
                "begin_period": portfolio_ref_date_start[key][key2]["value"],
                "end_period": portfolio_ref_date_end[key][key2]["value"],
            }
        reative_absolut_values = {"relative": relative_vals, "absolute": absolute_vals}
        return_dict[key] = reative_absolut_values

    return return_dict
