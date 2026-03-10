from django.shortcuts import render

from apps.backtests.models import Backtest

def home_view(request):
    recent_backtests = None

    if request.user.is_authenticated:
        recent_backtests = (
            Backtest.objects
            .filter(user=request.user)
            .order_by("-created_at")[:5]
        )

    if recent_backtests:
        print("Recent backtests:", recent_backtests[0])  # Debugging statement

    return render(request, "core/home.html", {"recent_backtests": recent_backtests})
