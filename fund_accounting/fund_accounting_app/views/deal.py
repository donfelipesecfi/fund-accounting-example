from rest_framework.viewsets import ModelViewSet
from fund_accounting_app.operations import book_deal
from fund_accounting_app.serializers import DealSerializer
from fund_accounting_app.models import Deal
from rest_framework.response import Response
from rest_framework import status


class DealView(ModelViewSet):

    allowed_methods = ["post", "get"]

    queryset = Deal.objects.all()
    serializer_class = DealSerializer

    def perform_create(self, serializer):
        import pdb

        pdb.set_trace()
        book_deal(**serializer.data)

    # def post(self, request):
    #     serializer = DealSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     deal = book_deal(serializer.data)
    #     return Response(DealSerializer(deal).data, status=status.HTTP_201_CREATED)
