from cmath import e
import json
import logging
import os
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect

from apps.strategies.models import Strategy
from apps.strategies.serializers import serialize_strategy
from apps.strategies.services.strategy_service import get_available_strategies_for_user, get_indicators

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def get_strategy_view(request):
    """
    View to retrieve strategies for the authenticated user.
    Retrieves both user-created and default strategies.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=401)

    try:
        strategies = get_available_strategies_for_user(request.user)

        data = [serialize_strategy(s) for s in strategies]

        return JsonResponse({"status": "success", "strategies": data})

    except Exception as e:
        logger.error(f"Error retrieving strategies: {e}", exc_info=True)
        return JsonResponse({"status": "error", "message": "Internal server error"}, status=500)


def get_indicator_list(request):
    """
    View to retrieve the list of available indicators from a static JSON file.
    """
    try:
        indicators = get_indicators()
        return JsonResponse({"status": "success", "indicators": indicators})

    except Exception as e:
        logger.error(f"Error retrieving indicators: {e}", exc_info=True)
        return JsonResponse({"status":"error","message": "Internal server error"}, status=500)


@csrf_protect
@require_http_methods(["POST"])
def save_strategy_view(request):
    """
    Docstring for save_strategy_view
    Json structure expected:
    {
        "name": "Strategy Name",
        "base_strategy_id": 1,
        "parameters": {
            ... strategy parameters ...
        }
    }
    """
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

    if not request.content_type == "application/json":
        return JsonResponse({"status": "error", "message": "Invalid content type"}, status=415)

    try:
        data = json.loads(request.body)
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    try:
        create_strategy = Strategy.objects.create(
            name=data.get("name", "Unnamed Strategy"),
            creator=request.user,
            base_strategy_id=data.get("base_strategy_id"),
            parameters=data.get("parameters", {}),
            is_default=False
        )
        
        return JsonResponse({
            "status": "success", 
            "strategy_id": create_strategy.pk,
            "message": "Strategy successfully saved"
        }, status=201)

    except Exception as err:
        logger.error(f"Error saving strategy: {err}", exc_info=True)
        return JsonResponse({
            "status": "error", 
            "message": "Nepodařilo se uložit strategii do DB."
        }, status=500)

@csrf_protect
@require_http_methods(["DELETE"])
def delete_strategy_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

    if not request.content_type == "application/json":
        return JsonResponse({"status": "error", "message": "Invalid content type"}, status=415)

    try:
        data = json.loads(request.body)
        strategy_id = data.get("strategy_id")
        if not strategy_id:
            return JsonResponse({"status": "error", "message": "Strategy ID is required"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    try:
        strategy = Strategy.objects.get(id=strategy_id, creator=request.user)
        strategy.delete()
        return JsonResponse({"status": "success", "message": "Strategy successfully deleted"}, status=200)

    except Strategy.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Strategy not found"}, status=404)

    except Exception as err:
        logger.error(f"Error deleting strategy: {err}", exc_info=True)
        return JsonResponse({
            "status": "error", 
            "message": "Failed to delete strategy from DB."
        }, status=500)