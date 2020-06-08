from rest_framework import serializers
from djmoney.models.fields import MoneyField
from secfi_common.serializers import CurrencySerializerField
from secfi_common.fields import Currency
from hordak.models import Money


class PositionsSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=10000)
    equity_value = CurrencySerializerField()
    fixed_income_value = CurrencySerializerField()
    total_collateral_shares = serializers.IntegerField()
    number_of_positions = serializers.IntegerField()

    def to_internal_value(self, data):
        for key in data.keys():
            if isinstance(data[key], Money):
                data[key] = Currency(
                    value=data[key].amount, currency=data[key].currency.code
                )
        return data


class PortfolioPositionsSerializer(serializers.Serializer):

    reference_date = serializers.DateField(format=None, input_formats=["%Y-%m-%d"])
