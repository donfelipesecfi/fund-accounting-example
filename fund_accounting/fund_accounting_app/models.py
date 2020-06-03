from django.db import models
from hordak.models import Account
import uuid


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
    # foreign keys
    company = models.UUIDField(null=False, blank=False)
    fund_manager = models.ForeignKey(FundManager, null=False, on_delete=models.CASCADE)
    # account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)

    eq_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False, related_name="eq_account"
    )
    eq_unrealized_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=False,
        related_name="eq_unrealized_account",
    )
    fi_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False, related_name="fi_account"
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

    @property
    def portfolio_equity(self):
        return int(round(self.total_collateral_shares * self.interest_equity, 0))
