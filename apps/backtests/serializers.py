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
        "trade_type": trade.trade_type,  # "buy" or "sell"
        "entry_time": trade.entry_time.isoformat() if trade.entry_time else None,
        "exit_time": trade.exit_time.isoformat() if trade.exit_time else None,
        "entry_price": float(trade.entry_price) if trade.entry_price is not None else None,
        "exit_price": float(trade.exit_price) if trade.exit_price is not None else None,
        "quantity": float(trade.quantity) if trade.quantity is not None else None,
        "stop_loss": float(trade.stop_loss) if trade.stop_loss is not None else None,
        "take_profit": float(trade.take_profit) if trade.take_profit is not None else None,
        "status": trade.status,  # "open" or "closed"
        "result": float(trade.result) if trade.result is not None else None,
    }


def serialize_backtest(backtest: Backtest) -> dict[str, Any]:
    return {
        "id": backtest.id,
        "user_id": backtest.user_id,
        "strategy": serialize_strategy(backtest.strategy),
        "asset": serialize_asset(backtest.asset) if backtest.asset else None,
        "timeframe": backtest.timeframe,
        "start_date": backtest.start_date.isoformat() if backtest.start_date else None,
        "end_date": backtest.end_date.isoformat() if backtest.end_date else None,
        "initial_capital": float(backtest.initial_capital),
        "created_at": backtest.created_at.isoformat() if backtest.created_at else None,
        "candles_amount": backtest.candles_amount,
        "result": backtest.result,
        "trades": [serialize_trade(t) for t in backtest.trades.all()],
    }