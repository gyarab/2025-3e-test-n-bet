import json
from venv import logger
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

from apps.backtests.models import Asset

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
def get_candles(request, token_id: int):
    """
    API endpoint to retrieve candle data for a specific token.
    Expects a JSON payload with parameters:
    {
        "interval": str (optional, default="1h"),
        "candle_amount": int (optional, default=100),
        "start_date": str (optional, ISO format date string)
    }
    """

    token = Asset.objects.filter(id=token_id).first()
    if not token:
        return JsonResponse(
            {"status": "error", "message": "Token not found"}, status=404
        )

    # Limit payload size to 1MB
    if len(request.body) > 1024 * 1024:
        return JsonResponse(
            {"status": "error", "message": "Payload too large"}, status=413
        )
    
    try:
        from apps.market.services import get_binance_ohlcv_and_timestamp

        payload = json.loads(request.body) if request.body else {}
        token = token.symbol

        interval = payload.get("interval", "1h")
        candle_amount = payload.get("candle_amount", 100)
        start_date = payload.get("start_date")

        if not token:
            return JsonResponse(
                {"status": "error", "message": "token is required"}, status=400
            )
        
        if start_date:
            from datetime import datetime
            try:
                start_date = datetime.fromisoformat(start_date)
            except ValueError:
                return JsonResponse(
                    {"status": "error", "message": "Invalid start_date format"}, status=400
                )

        candles = get_binance_ohlcv_and_timestamp(token, interval, candle_amount, start_date=start_date)

        return JsonResponse({"status": "success", "candles": candles}, status=200)
    except Exception as err:
        logger.error(f"Error retrieving candle data: {err}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"Error: {str(err)}"}, status=500
        )
    

@require_http_methods(["POST"])
def get_candles_in_range(request, token_id: int):
    """
    API endpoint to retrieve candle data for a specific token within a date range.
    Expects a JSON payload with parameters:
    {
        "interval": str (optional, default="1h"),
        "start_date": str (required, ISO format date string),
        "end_date": str (required, ISO format date string)
    }
    """

    token = Asset.objects.filter(id=token_id).first()
    if not token:
        return JsonResponse(
            {"status": "error", "message": "Token not found"}, status=404
        )

    # Limit payload size to 1MB
    if len(request.body) > 1024 * 1024:
        return JsonResponse(
            {"status": "error", "message": "Payload too large"}, status=413
        )
    
    try:
        from apps.market.services import get_binance_ohlcv_and_timestamp_range

        payload = json.loads(request.body) if request.body else {}
        token = token.symbol

        print(f"Received payload: {payload}")

        interval = payload.get("interval", "1h")
        start_date = payload.get("start_date")
        end_date = payload.get("end_date")

        if not token:
            return JsonResponse(
                {"status": "error", "message": "token is required"}, status=400
            )
        
        if start_date and end_date:
            from datetime import datetime
            try:
                start_date = datetime.fromisoformat(start_date)
                end_date = datetime.fromisoformat(end_date)
            except ValueError:
                return JsonResponse(
                    {"status": "error", "message": "Invalid date time formats. ISO style is required."}, status=400
                )
        
        candles = get_binance_ohlcv_and_timestamp_range(token, interval, start_date=start_date, end_date=end_date)

        return JsonResponse({"status": "success", "candles": candles}, status=200)
    except Exception as err:
        logger.error(f"Error retrieving candle data: {err}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"Error: {str(err)}"}, status=500
        )