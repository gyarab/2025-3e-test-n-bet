from cmath import e
import json
import logging
import os
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect

from apps.strategies.models import Strategy

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def get_strategy_view(request):
    """
    View to retrieve strategies for the authenticated user.
    Retrieves both user-created and default strategies.
    """
    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=401)

    try:
        # Django ORM query to get strategies. Q object is used for complex queries.
        strategies = strategies = Strategy.objects.filter(
            Q(creator=request.user) | Q(creator__isnull=True)
        ).order_by("id")

        data = [
            {
                "id": s.id,
                "name": s.name,
                "creator_id": s.creator_id,
                "base_strategy_id": s.base_strategy_id,
                "parameters": s.parameters,
                "is_default": s.is_default,
                "created_at": s.created_at.isoformat(),
            }
            for s in strategies
        ]

        return JsonResponse({"status": "success", "strategies": data})

    except Exception as e:
        logger.error(f"Error retrieving strategies: {e}", exc_info=True)
        return JsonResponse({"status": "error", "message": "Internal server error"}, status=500)


def get_indicator_list(request):
    """
    View to retrieve the list of available indicators from a static JSON file.
    """
    try:
        json_path = os.path.join('apps', 'strategies', 'static', 'strategies', 'strategy_builder', 'indicators.json')
        with open(json_path, 'r') as f:
            indicators = json.load(f)

        return JsonResponse({"status": "success", "indicators": indicators})

    except Exception as e:
        logger.error(f"Error retrieving indicators: {e}", exc_info=True)
        return JsonResponse({"status":"error","message": "Internal server error"}, status=500)

@csrf_protect
@require_http_methods(["POST"])
def save_strategy_view(request):
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
            "strategy_id": create_strategy.id,
            "message": "Strategy successfully saved"
        }, status=201)

    except Exception as err:
        logger.error(f"Error saving strategy: {err}", exc_info=True)
        return JsonResponse({
            "status": "error", 
            "message": "Nepodařilo se uložit strategii do DB."
        }, status=500)