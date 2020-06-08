from rest_framework import serializers


class PortfolioRequestSerializer(serializers.Serializer):

    reference_date_start = serializers.DateField(
        format=None, input_formats=["%Y-%m-%d"]
    )
    reference_date_end = serializers.DateField(format=None, input_formats=["%Y-%m-%d"])
