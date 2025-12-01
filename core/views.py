from django.shortcuts import render

from apps.market.services import get_market_summary

def home_view(request):
    # summary = get_market_summary(['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'BNB/USDT', 'SOL/USDT'])
    return render(request, 'core/home.html')