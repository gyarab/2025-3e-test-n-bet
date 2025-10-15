# tests/test_backtest_sma_functional.py
import pytest
from apps.strategies.services.strategies.sma_strategy import SMAStrategy
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.strategies.services.core.strategy_engine import StrategyEngine
from apps.strategies.services.core.strategy_condition import StrategyCondition
from apps.backtests.services.backtest_engine import BacktestEngine

def generate_uptrend_candles(n: int, start_price: float = 100.0, step: float = 1.0):
    """
    Generate a deterministic uptrend to trigger SMA BUY signal.
    Each candle closes slightly higher than the previous.
    """
    candles = []
    price = start_price
    for _ in range(n):
        open_p = price
        close = price + step
        high = close + 0.5
        low = open_p - 0.5
        volume = 1000
        candles.append({
            "open": open_p,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume
        })
        price = close
    return candles

def test_backtest_sma_long_trade_executed():
    """
    Functional test: one SMA strategy on uptrend candles
    should trigger a BUY and execute trades.
    """

    # Generate 50 candles in uptrend
    candles = generate_uptrend_candles(50, start_price=100, step=1)

    # Create SMA strategy (short < long to ensure crossover)
    sma_strategy = SMAStrategy.from_parametrs(short_window=3, long_window=5)

    # Simple risk model
    risk_model = TradeRiskModel(stop_loss_pct=1, take_profit_pct=2)

    # Condition using only SMA
    condition = StrategyCondition(
        strategy_list=[sma_strategy],
        buy_risk_model=risk_model,
        sell_risk_model=risk_model,  # optional for this test
        do_action_if_buy=True,
        do_action_if_sell=False
    )

    # Strategy engine with this single condition
    engine = StrategyEngine(conditions=[], trade_risk_model=risk_model)
    engine.add_condition(condition)

    # Backtest engine
    backtest = BacktestEngine(strategy=engine, trade_risk_model=risk_model, candles=None, initial_balance=1000)
    backtest.candles = candles  # inject our deterministic candles

    # Run backtest
    final_balance, trades = backtest.run()

    # Assertions
    assert trades, "Expected at least one trade to be executed"
    for trade in trades:
        assert trade.entry_price > 0
        result = trade.get_result()
        # Trade result could be -1 if last candle didn't close trade, but we can check exit price exists if closed
        if result != -1:
            assert isinstance(result, (int, float))
    
    # Final balance should be numeric
    assert isinstance(final_balance, (int, float))
    print("Final balance:", final_balance)
    print("Trades executed:", len(trades))
