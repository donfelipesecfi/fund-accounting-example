from hordak.utilities.currency import Balance


def convert_balance_to_money_usd(balance: Balance):
    return balance.__getitem__("USD")
