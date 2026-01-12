import json
from venv import logger
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def  get_hot_tokens(request):
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
        return JsonResponse({"status": "error", "message": "Payload too large"}, status=413)

    try:
        from apps.market.services import get_hot_coins

        payload = json.loads(request.body) if request.body else {}

        hot_coins = get_hot_coins(threshold_change=payload.get("threshold_change", 5.0), 
                                  only_positive=payload.get("only_positive", True), 
                                  limit=payload.get("limit", 10))

        return JsonResponse({
            "status": "success",
            "hot_tokens": hot_coins
        }, status=200)

    except Exception as err:
        logger.error(f"Error retrieving hot tokens: {err}", exc_info=True)
        return JsonResponse({
            "status": "error",
            "message": f"Error: {str(err)}"
        }, status=500)