from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.strategies.serializers import serialize_strategy
from apps.strategies.services.strategy_service import get_available_strategies_for_user

@login_required  
def backtests_home(request):
    strategies = get_available_strategies_for_user(request.user)
    serialized_strategies = [serialize_strategy(s) for s in strategies]
    return render(request, "backtests/pages/backtests.html", {
        'strategies': serialized_strategies,
    })
