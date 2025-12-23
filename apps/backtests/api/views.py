import json
import logging
from django.http import JsonResponse
from apps.strategies.models import Strategy
from django.views.decorators.csrf import csrf_protect
from apps.backtests.services.services import run_backtest

from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

@csrf_protect
@require_http_methods(["POST"])
def run_backtest_view(request):
    """
    View to run a backtest for a given strategy. 
    Expects a JSON body with the following structure:
    {
        "strategy_id": int,
        "initial_balance": float (optional, default=1000),
        "token": str (optional, default="BTC"),
        "timeframe": str (optional, default="1h"),
        "candle_amount": int (optional, default=500)
    }
    Returns a JSON response with the backtest results.
    """

    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=401)
    
    # Check content type
    if not request.content_type.startswith("application/json"):
        return JsonResponse({"status": "error", "message": "Expected application/json"}, status=415)
    
    # Limit payload size to 1MB
    if len(request.body) > 1024 * 1024:
        return JsonResponse({"status": "error", "message": "Payload too large"}, status=413)

    # Parse JSON body
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    # Get strategy ID from payload
    try:
        strategy_id = int(payload.get("strategy_id"))
    except (KeyError, TypeError, ValueError):
        return JsonResponse({"status": "error", "message": "Invalid strategy_id"}, status=400)
    
    # Run backtest
    try:
        strategy = Strategy.objects.get(id=strategy_id)

        print("Strategy found:", strategy)

        result = run_backtest(
            user=request.user,
            strategy=strategy,
            initial_balance=payload.get("initial_balance", 1000),
            token=payload.get("token", "BTCUSDT"),
            timeframe=payload.get("timeframe", "1h"),
            candle_amount=payload.get("candle_amount", 500)
        )

        return JsonResponse({"status": "success", "result": result})

    except Strategy.DoesNotExist:
        return JsonResponse({"status":"error","message":"Strategy not found"}, status=404)
    except Exception as e:
        logger.error(f"Error running backtest: {e}", exc_info=True)
        return JsonResponse({"status":"error","message": "Internal server error"}, status=500)

