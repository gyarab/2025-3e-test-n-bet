from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.strategies.serializers import serialize_strategy
from apps.strategies.services.strategy_service import get_available_strategies_for_user
from apps.backtests.serializers import serialize_backtest
from apps.backtests.services.services import get_available_backtests, get_backtest


@login_required
def backtests_home(request):
    strategies = get_available_strategies_for_user(request.user)

    serialized_strategies = None
    if strategies:
        serialized_strategies = [serialize_strategy(s) for s in strategies]

    return render(
        request,
        "backtests/pages/backtests.html",
        {
            "strategies": serialized_strategies,
        },
    )

@login_required
def backtest_detail(request, backtest_id: int):
    backtest = get_backtest(request.user, backtest_id)

    serialized_backtest = None
    if backtest:
        serialized_backtest = serialize_backtest(backtest)

    print(serialized_backtest)

    return render(
        request,
        "backtests/pages/backtest_detail.html",
        {
            "backtest": serialized_backtest,
        },
    )

@login_required
def my_backtests(request):
    backtests = get_available_backtests(request.user)

    serialized_backtests = None
    if backtests:
        serialized_backtests = [serialize_backtest(b) for b in backtests]

    return render(
        request,
        "backtests/pages/my_backtests.html",
        {
            "backtests": serialized_backtests,
        },
    )