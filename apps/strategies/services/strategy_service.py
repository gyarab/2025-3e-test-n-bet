from django.db.models import Q
from ..models import Strategy
import os
import json

def get_available_strategies_for_user(user) -> list[Strategy]:
    """
    Returns user-created strategies + default strategies. Does not include errors.
    """
    if not user.is_authenticated:
        return Strategy.objects.filter(creator__isnull=True).order_by("id")
    
    return Strategy.objects.filter(
        Q(creator=user) | Q(creator__isnull=True)
    ).order_by("id")

def get_indicators() -> list:
    """
    Returns the list of available indicators from a static JSON file.
    """
    json_path = os.path.join('apps', 'strategies', 'static', 'strategies', 'indicators.json')
    with open(json_path, 'r') as f:
        indicators = json.load(f)

    return indicators
