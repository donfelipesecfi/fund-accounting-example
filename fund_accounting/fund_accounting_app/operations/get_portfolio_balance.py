from hordak.models import Account


def get_top_level_portfolio_balance(pf_number):

    cash_account = Account.objects.get(code=f"B{pf_number}")
    print(cash_account.balance())
    eq_account = Account.objects.get(code=f"C{pf_number}")
    print(eq_account.balance())
    fi_account = Account.objects.get(code=f"D{pf_number}")
    print(fi_account.balance())
