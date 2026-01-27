from django.shortcuts import render
import os
import json

from apps.strategies.services.strategy_service import get_available_strategies_for_user
from apps.strategies.serializers import serialize_strategy
from .models import Strategy

def strategy(request):
    strategies = get_available_strategies_for_user(request.user)
    serialized_strategies = [serialize_strategy(s) for s in strategies]
    return render(request, "strategies/pages/strategy.html", {
        'strategies': serialized_strategies,
    })



# TODO: Implement views for getting strategy results (get_sma_list and get_sma_result in strategies/sma.py).