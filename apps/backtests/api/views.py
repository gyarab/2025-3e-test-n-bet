import json
import logging
from django.http import JsonResponse
from apps.strategies.models import Strategy
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from apps.backtests.services.services import run_backtest
from apps.backtests.models import Backtest, Asset
# from ccxt.base.errors import RequestTimeout

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

        result = run_backtest(
            user=request.user,
            strategy=strategy,
            initial_balance=payload.get("initial_balance", 1000),
            token=payload.get("token", "BTCUSDT"),
            timeframe=payload.get("timeframe", "1h"),
            candle_amount=payload.get("candle_amount", 500),        )
        return JsonResponse({"status": "success", "result": result})
    
    except Strategy.DoesNotExist:
        return JsonResponse({"status":"error","message":"Strategy not found"}, status=404)
    except Exception as e:
        logger.error(f"Error running backtest: {e}", exc_info=True)
        return JsonResponse({"status":"error","message": "Internal server error"}, status=500)
    except RuntimeError as e:
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=504
        )


logger = logging.getLogger(__name__)

@require_http_methods(["POST"])
def save_backtest_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

    try:
        data = json.loads(request.body)
        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        token_symbol = data.get("asset_id")  
      
        asset_obj, created = Asset.objects.get_or_create(
            symbol=token_symbol,
            defaults={'name': token_symbol} 
        )

        backtest = Backtest.objects.create(
            user=request.user,
            strategy_id=data.get("strategy_id"),
            
            asset=asset_obj,  
            
            result=data.get("result", {}),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            initial_capital=data.get("initial_capital"),
            position_size=data.get("position_size"),
        )

        return JsonResponse({
            "status": "success", 
            "backtest_id": backtest.id,
            "message": "Backtest successfully saved"
        }, status=201)

    except Exception as err:
        logger.error(f"Error saving backtest: {err}", exc_info=True)
        return JsonResponse({
            "status": "error", 
            "message": f"Error: {str(err)}"
        }, status=500)
    
@require_http_methods(["GET"])
def get_user_backtest(request):
    """
    Retrieves backtests filtered by user_id if provided.
    """
 
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=401)

    user = request.user

    try:
        backtests = Backtest.objects.filter(user=user)

        data = [
            {
                "id": b.id,
                "user_id": b.user.id,

                "strategy": {
                    "id": b.strategy_id,
                    "name": b.strategy.name,
                    "parameters": b.strategy.parameters,
                },

                "asset": {
                    "id": b.asset_id,
                    "symbol": b.asset.symbol,
                    "name": b.asset.name,
                },

                "start_date": b.start_date.isoformat() if b.start_date else None,
                "end_date": b.end_date.isoformat() if b.end_date else None,
                "initial_capital": b.initial_capital,
                "position_size": b.position_size,
                "created_at": b.created_at.isoformat() if b.created_at else None,

                "trades": [
                    {
                        "id": t.id,
                        "time": t.time.isoformat(),
                        "price": t.price,
                        "quantity": t.quantity,
                        "profit": t.profit,
                        "type": "BUY" if t.is_buy else "SELL",
                    }
                    for t in b.trades.all()
                ],
            }
            for b in backtests
        ]

        return JsonResponse({"status": "success", "backtests": data})

    except Exception as e:
        logger.error(f"Error retrieving strategies: {e}", exc_info=True)
        return JsonResponse({"status": "error", "message": "Internal server error"}, status=500)
