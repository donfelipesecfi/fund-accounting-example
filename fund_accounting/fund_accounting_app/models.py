from django.db import models
from hordak.models import Account
import uuid
from decimal import Decimal


class FundManager(models.Model):
    """
    The FundManager model represents the fund manager of one associated account.
    """

    name = models.CharField(max_length=251, blank=False)
    fund = models.UUIDField(null=False, blank=False)
    fund_number = models.PositiveIntegerField(null=False, blank=False)
    hurdle = models.DecimalField(max_digits=10, decimal_places=4)

    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)

    def save(self):

        if not self.account.type == "EQ":
            raise Exception(
                "Fund Manager needs to have assoicated account of type Equity."
            )
        super().save()


class Deal(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4)
    date = models.DateField(null=False)

    # foreign keys
    company = models.UUIDField(null=False, blank=False)
    company_name = models.CharField(max_length=200)
    fund_manager = models.ForeignKey(FundManager, null=False, on_delete=models.CASCADE)

    eq_account_value = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False, related_name="eq_account_value"
    )

    eq_account_stock = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False, related_name="eq_account_stock"
    )

    eq_unrealized_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=False,
        related_name="eq_unrealized_account",
    )

    fi_account_value = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False, related_name="fi_account_value"
    )

    fi_account_stock = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False, related_name="fi_account_stock"
    )

    fi_unrealized_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=False,
        related_name="fi_unrealized_account",
    )

    # financials
    # TODO MAKE CURRENCY FIELD LATER!
    total_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_collateral_shares = models.PositiveIntegerField()

    interest_loan = models.DecimalField(
        max_digits=8, decimal_places=4, null=False, blank=False
    )
    interest_equity = models.DecimalField(
        max_digits=8, decimal_places=4, null=False, blank=False
    )

    last_booking_interest = models.DateTimeField(null=True)
    last_booking_equity_valuation = models.DateTimeField(null=True)

    @property
    def portfolio_equity(self):

        return int(
            round(self.total_collateral_shares * Decimal(self.interest_equity), 0)
        )

    def total_portfolio_value_equity(self, date):
        return self.eq_account_stock.balance(as_of=date).__getitem__(
            "USD"
        ) + self.eq_account_value.balance(as_of=date).__getitem__("USD")

    def total_portfolio_value_fixed_income(self, date):
        return self.eq_account_stock.balance(as_of=date).__getitem__(
            "USD"
        ) + self.eq_account_value.balance(as_of=date).__getitem__("USD")

    def total_portfolio_value(self, date):

        return self.total_portfolio_value_equity(date).__getitem__(
            "USD"
        ) + self.total_portfolio_value_fixed_income(date).__getitem__("USD")
