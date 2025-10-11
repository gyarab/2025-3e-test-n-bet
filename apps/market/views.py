# apps/market/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .data_store import get_prices

class BtcPricesView(APIView):
    def get(self, request):
        # vrátí všechny ticky, které jsou aktuálně v paměti
        prices = get_prices()
        return Response(prices)
