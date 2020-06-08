from rest_framework.viewsets import ViewSet
from fund_accounting_app.operations import book_deal
from fund_accounting_app.serializers import (
    DealSerializer,
    PortfolioRequestSerializer,
    PortfolioPositionsSerializer,
    PositionsSerializer,
)
from fund_accounting_app.models import Deal, FundManager
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from fund_accounting_app.operations.get_portfolio_balance import (
    get_top_level_portfolio_returns,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer


class PortfolioView(ViewSet):
    @swagger_auto_schema(query_serializer=PortfolioRequestSerializer)
    @action(methods=["GET"], detail=True)
    def returns(self, request, *args, **kwargs):

        serializer = PortfolioRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query_set = self.get_queryset(fund_manager__fund_number=kwargs["pk"])
        import pdb

        pdb.set_trace()
        calculated_returns = get_top_level_portfolio_returns(
            kwargs["pk"], **serializer.data, add_absolute_values=False
        )
        import pdb

        return Response(calculated_returns)

    @swagger_auto_schema(request_body=DealSerializer)
    @action(methods=["POST"], detail=True)
    def add_deal(self, request, *args, **kwargs):

        serializer = DealSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query_set = self.get_queryset(fund_manager__fund_number=kwargs["pk"])

        #  TODO: ADD PRICE NOT HARDCODED
        deal_added = book_deal(**{**serializer.data, "value_per_share": 0.2})

        return Response(DealSerializer(instance=deal_added).data)

    @swagger_auto_schema(query_serializer=PortfolioPositionsSerializer)
    @action(methods=["GET"], detail=True)
    def postitions(self, request, *args, **kwargs):

        serializer = PortfolioPositionsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        aggregated_value = self.get_position_values_per_company(
            serializer.data["reference_date"],
            self.get_queryset(fund_manager__fund_number=kwargs["pk"]),
        )

        positions_serializer = PositionsSerializer(data=aggregated_value, many=True)
        positions_serializer.is_valid()

        return Response(positions_serializer.data)

    def get_queryset(self, **kwargs):
        return Deal.objects.filter(**kwargs).all()

    def get_position_values_per_company(self, date, queryset):

        company_values = []
        distinct_companies = queryset.values("company").distinct()
        for company in distinct_companies:

            sum_equity_value = sum(
                [
                    deal.total_portfolio_value_equity(date)
                    for deal in queryset.filter(**company)
                ]
            )
            sum_fixed_income_value = sum(
                [
                    deal.total_portfolio_value_equity(date)
                    for deal in queryset.filter(**company)
                ]
            )

            sum_total_collateral_shares = sum(
                [deal.total_collateral_shares for deal in queryset.filter(**company)]
            )

            number_of_positions = queryset.filter(**company).count()

            company_values.append(
                {
                    "name": str(company["company"]),
                    "equity_value": sum_equity_value,
                    "fixed_income_value": sum_fixed_income_value,
                    "total_collateral_shares": sum_total_collateral_shares,
                    "number_of_positions": number_of_positions,
                }
            )

        return company_values
