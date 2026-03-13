import json
from venv import logger
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
def get_hot_tokens(request):
    """
    API endpoint to retrieve hot tokens from the market service.
    Expects a JSON payload with optional parameters:
    {
        "threshold_change": float (optional, default=5.0),
        "only_positive": bool (optional, default=True),
        "limit": int (optional, default=10)
    }
    """

    # Limit payload size to 1MB
    if len(request.body) > 1024 * 1024:
        return JsonResponse(
            {"status": "error", "message": "Payload too large"}, status=413
        )

    try:
        from apps.market.services import get_hot_coins

        payload = json.loads(request.body) if request.body else {}

        hot_coins = get_hot_coins(
            threshold_change=payload.get("threshold_change", 5.0),
            only_positive=payload.get("only_positive", True),
            limit=payload.get("limit", 10),
        )

        return JsonResponse({"status": "success", "hot_tokens": hot_coins}, status=200)

    except Exception as err:
        logger.error(f"Error retrieving hot tokens: {err}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"Error: {str(err)}"}, status=500
        )

@require_http_methods(["POST"])
def get_candles(request):
    """
    API endpoint to retrieve candle data for a specific token.
    Expects a JSON payload with parameters
    """

    # Limit payload size to 1MB
    if len(request.body) > 1024 * 1024:
        return JsonResponse(
            {"status": "error", "message": "Payload too large"}, status=413
        )
    
    try:
        from apps.market.services import get_binance_ohlcv_and_timestamp

        payload = json.loads(request.body) if request.body else {}
        token = payload.get("token")
        interval = payload.get("interval", "1h")
        candle_amount = payload.get("candle_amount", 100)
        
        if not token:
            return JsonResponse(
                {"status": "error", "message": "token is required"}, status=400
            )

        candles = get_binance_ohlcv_and_timestamp(token, interval, candle_amount)

        return JsonResponse({"status": "success", "candles": candles}, status=200)
    except Exception as err:
        logger.error(f"Error retrieving candle data: {err}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"Error: {str(err)}"}, status=500
        )