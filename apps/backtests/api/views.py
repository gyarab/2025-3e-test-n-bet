from django.http import JsonResponse
from apps.strategies.models import Strategy
from .services import run_backtest

from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def run_backtest_view(request):
    try:
        strategy_id = request.GET.get("strategy_id") or (request.POST.get("strategy_id") if request.method=="POST" else None)
        if not strategy_id:
            return JsonResponse({"status":"error","message":"strategy_id missing"}, status=400)

        strategy = Strategy.objects.get(id=strategy_id)
        result = run_backtest(
            user=None,  
            strategy=strategy,
            initial_balance=1000,
            token="BTC",
            timeframe="1h",
            candle_amount=500
        )

        return JsonResponse({"status": "success", "result": result})

    except Strategy.DoesNotExist:
        return JsonResponse({"status":"error","message":"Strategy not found"}, status=404)
    except Exception as e:
        return JsonResponse({"status":"error","message": str(e)}, status=500)

