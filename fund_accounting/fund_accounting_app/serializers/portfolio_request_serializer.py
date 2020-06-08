from rest_framework import serializers


class PortfolioRequestSerializer(serializers.Serializer):

    reference_date_start = serializers.DateField(input_formats=["%Y-%m-%d"])
    reference_date_end = serializers.DateField(input_formats=["%Y-%m-%d"])

