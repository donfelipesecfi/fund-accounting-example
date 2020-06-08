from rest_framework.viewsets import ViewSet
from fund_accounting_app.operations import book_deal
from fund_accounting_app.serializers import DealSerializer, PortfolioRequestSerializer
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
    # @swagger_auto_schema(method="GET", query_serializer=PortfolioRequestSerializer)

    # @action(methods=["GET"], detail=True)
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(query_serializer=PortfolioRequestSerializer)
    @action(methods=["GET"], detail=True)
    def returns(self, request, *args, **kwargs):

        serializer = PortfolioRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query_set = self.get_queryset(fund_manager__fund_number=kwargs["pk"])

        calculated_returns = get_top_level_portfolio_returns(
            kwargs["pk"], **serializer.data
        )
        import pdb

        pdb.set_trace()

        return Response(calculated_returns)

    @swagger_auto_schema(query_serializer=PortfolioRequestSerializer)
    @action(methods=["GET"], detail=True)
    def add_deal(self, request, *args, **kwargs):

        serializer = PortfolioRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query_set = self.get_queryset(fund_manager__fund_number=kwargs["pk"])

        calculated_returns = get_top_level_portfolio_returns(
            kwargs["pk"], **serializer.data
        )
        import pdb

        pdb.set_trace()

        return Response(calculated_returns)

    def get_queryset(self, **kwargs):
        return Deal.objects.filter(**kwargs).all()
