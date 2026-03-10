from typing import Any

from apps.backtests.models import Asset, Backtest, Trade
from apps.strategies.serializers import serialize_strategy


def serialize_asset(asset: Asset) -> dict[str, Any]:
    return {
        "id": asset.id, 
        "symbol": asset.symbol,
        "name": asset.name,
    }


def serialize_trade(trade: Trade) -> dict[str, Any]:
    return {
        "id": trade.id,
        "time": trade.time.isoformat(),
        "price": float(trade.price),
        "is_buy": trade.is_buy,
        "quantity": float(trade.quantity),
        "profit": float(trade.profit),
    }


def serialize_backtest(backtest: Backtest) -> dict[str, Any]:
    return {
        "id": backtest.id,
        "user_id": backtest.user_id,
        "strategy": serialize_strategy(backtest.strategy),
        "asset": serialize_asset(backtest.asset) if backtest.asset else None,
        "start_date": backtest.start_date.isoformat() if backtest.start_date else None,
        "end_date": backtest.end_date.isoformat() if backtest.end_date else None,
        "initial_capital": float(backtest.initial_capital),
        "position_size": float(backtest.position_size) if backtest.position_size else None,
        "created_at": backtest.created_at.isoformat() if backtest.created_at else None,
        "result": backtest.result,
        "trades": [serialize_trade(t) for t in backtest.trades.all()],
    }