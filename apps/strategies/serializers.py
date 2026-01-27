from apps.strategies.models import Strategy


def serialize_strategy(strategy: Strategy) -> dict:
    return {
        "id": strategy.pk,
        "name": strategy.name,
        "creator_id": strategy.creator.pk if strategy.creator else None,
        "base_strategy_id": strategy.base_strategy.pk if strategy.base_strategy else None,
        "parameters": strategy.parameters,
        "is_default": strategy.is_default,
        "created_at": strategy.created_at.isoformat(),
    }