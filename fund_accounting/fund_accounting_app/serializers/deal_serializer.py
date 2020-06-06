from rest_framework.serializers import ModelSerializer
from fund_accounting_app.models import Deal


class DealSerializer(ModelSerializer):
    class Meta:
        model = Deal
        fields = [
            "date",
            "company_name",
            "fund_manager",
            "company",
            "total_loan_amount",
            "total_collateral_shares",
            "interest_loan",
            "interest_equity",
        ]
