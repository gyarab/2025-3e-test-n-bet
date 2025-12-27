import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from apps.strategies.models import Strategy

logger = logging.getLogger(__name__)

@csrf_protect
@require_http_methods(["GET"])
def get_strategy_view(request):
    """
    Retrieves strategies filtered by creator_id if provided.
    If no creator_id is given, returns all strategies.
    """

    
    creator_id = request.GET.get("creator_id") # Can be None

    try:
        # Decide which strategies to return
        if creator_id:
            strategies = Strategy.objects.filter(creator_id=creator_id)
        else:
            strategies = Strategy.objects.filter(creator__isnull=True)

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
