from django.core.exceptions import PermissionDenied

from apps.strategies.services.core.strategy_engine import StrategyEngine
from apps.strategies.models import Strategy
from apps.market.services import get_binance_ohlcv
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from .backtest.backtest_engine import BacktestEngine
from ccxt.base.errors import RequestTimeout
from ccxt.base.errors import RequestTimeout




def run_backtest(user, strategy: Strategy, initial_balance: float = 1000, token: str = 'BTCUSDT', timeframe: str = '1h', candle_amount: int = 500) -> dict:
    """
    Application service entry point.
    """
    
    
    if(not strategy.creator is None):
        if(user.id != strategy.creator_id and not user.is_staff and not user.is_superuser):
            raise PermissionDenied("User does not have permission to run this strategy.")
    
    try:
        initial_balance = float(initial_balance)
        candle_amount = int(candle_amount)
    except ValueError:
        raise ValueError("Initial balance must be a float and candle amount must be an integer.")

    srategy_engine = StrategyEngine._from_parameters(strategy.parameters)
    try:
        candles =  get_binance_ohlcv(token, timeframe, candle_amount)
    except RequestTimeout as e:
        raise RuntimeError("Market data timeout") from e

    backtest = BacktestEngine(strategy=srategy_engine, initial_balance=initial_balance, candles=candles)

    current_balance, self_trades = backtest.run()

    return {
        "initial_balance": initial_balance,
        "final_balance": current_balance,
        "profit_loss": current_balance - initial_balance,
        "token": token,
        "timeframe": timeframe,
        "total_trades": len(self_trades),
        "total_wins": len([trade for trade in self_trades if trade.get_result() and trade.get_result() > 0]),
        "total_losses": len([trade for trade in self_trades if trade.get_result() and trade.get_result() <= 0]),
        "not_closed_trades": len([trade for trade in self_trades if trade.get_result() is None]),
        "trades": [trade.get_json() for trade in self_trades],
    }