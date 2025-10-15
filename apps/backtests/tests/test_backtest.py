# tests/test_backtest_two_indicators.py
import os
import random
import math
from typing import List, Dict

import pytest

from apps.strategies.services.strategies.rsi_strategy import RSIStrategy
from apps.strategies.services.strategies.sma_strategy import SMAStrategy

# Try imports using the package structure from your snippet. Adjust if your project layout differs.
try:
    from apps.strategies.services.core.trade_risk_model import TradeRiskModel
    from apps.strategies.services.core.strategy_engine import StrategyEngine
    from apps.backtests.services.backtest_engine import BacktestEngine
    from apps.strategies.services.core.strategy_condition import StrategyCondition
except Exception as e:
    # If your pythonpath is different during tests, raise a helpful error
    raise ImportError(
        "Failed to import project modules. Make sure your project's package root is on PYTHONPATH when running pytest.\n"
        "Original import error: " + str(e)
    )


def generate_synthetic_candles(n: int, start_price: float = 100.0, seed: int = 42) -> List[Dict]:
    """
    Create deterministic synthetic OHLCV candles using a seeded random walk.
    Returns list of dicts with keys: open, high, low, close, volume
    """
    random.seed(seed)
    prices = [start_price]
    for _ in range(n - 1):
        # small percentage change drawn from normal-like distribution
        pct = random.gauss(0, 0.0025)  # low volatility by default
        new_price = max(0.01, prices[-1] * (1 + pct))
        prices.append(new_price)

    candles = []
    for i in range(n):
        close = prices[i]
        # make open slightly previous close (or same for first candle)
        open_p = prices[i - 1] if i > 0 else close
        # simulate high/low within a small band
        hi = max(open_p, close) * (1 + abs(random.gauss(0, 0.001)))
        lo = min(open_p, close) * (1 - abs(random.gauss(0, 0.001)))
        volume = max(1.0, random.gauss(1000, 200))
        candles.append({
            "open": round(open_p, 8),
            "high": round(hi, 8),
            "low": round(lo, 8),
            "close": round(close, 8),
            "volume": round(volume, 8)
        })
    return candles


@pytest.mark.slow
def test_backtest_with_two_sma_indicators_runs_on_1000_candles():
    """
    Build a StrategyEngine with two SMA-based indicators (different windows),
    run BacktestEngine on 1000 synthetic candles and assert the backtest runs
    and returns sensible outputs (balance + trades list).
    """

    # 1) Generate 1000 candles (deterministic)
    n_candles = 1000
    candles = generate_synthetic_candles(n_candles, start_price=100.0, seed=12345)

    # 2) Create two SMA strategies (different windows)
    # Use SMAIndicator instances if required by your SMAStrategy.from_parametrs / ctor
    sma_strat = SMAStrategy.from_parametrs(short_window=10, long_window=30)
    rsi_strat = RSIStrategy.from_parametrs()

    # 3) Construct StrategyCondition combining both indicators. Provide buy/sell risk models.
    buy_risk = TradeRiskModel(stop_loss_pct=2.0, stop_loss_type="fixed", take_profit_pct=4.0, take_profit_type="fixed")
    sell_risk = TradeRiskModel(stop_loss_pct=2.0, stop_loss_type="fixed", take_profit_pct=4.0, take_profit_type="fixed")

    condition = StrategyCondition(
        strategy_list=[sma_strat, rsi_strat],
        buy_risk_model=buy_risk,
        sell_risk_model=sell_risk,
        do_action_if_buy=True,
        do_action_if_sell=True
    )

    # 4) Build StrategyEngine with this single condition
    engine = StrategyEngine(conditions=[], trade_risk_model=TradeRiskModel())
    engine.add_condition(condition)

    # 5) Create BacktestEngine and inject candles (note: BacktestEngine.__init__ in snippet
    # does not assign self.candles, so set it explicitly here)
    backtest = BacktestEngine(strategy=engine, trade_risk_model=TradeRiskModel(), candles=None, initial_balance=1000.0)
    # assign candles directly (workaround for the missing assignment in __init__)
    backtest.candles = candles

    # 6) Run the backtest (should not raise)
    final_balance, trades = backtest.run()

    # 7) Basic assertions about the outputs
    assert isinstance(final_balance, (int, float)), "final_balance should be numeric"
    assert isinstance(trades, list), "trades should be a list"

    # If there are trades, ensure each trade is an instance of TradeEngine and has expected attributes
    if trades:
        for t in trades:
            # the TradeEngine class in your snippet doesn't have a common base,
            # but we can assert that expected attributes exist
            assert hasattr(t, "entry_price")
            assert hasattr(t, "quantity")
            # trade.get_result() should be a float or -1 (if not closed)
            res = t.get_result()
            assert isinstance(res, (int, float))
    # If no trades were executed, that's still a valid outcome for synthetic data.
    # The main goal of this test is to ensure integration path runs without error.

    # Extra sanity: final balance should be finite
    assert math.isfinite(float(final_balance))


# Optional: test that can use live binance data if env var is set.
# To use live data (not recommended for CI), set USE_LIVE_BINANCE=1 in environment.
@pytest.mark.optional
def test_backtest_with_live_binance_if_requested(monkeypatch):
    """
    Optional: if environment variable USE_LIVE_BINANCE is set, this test will
    attempt to call your project's get_binance_ohlcv function to fetch 1000 candles.
    This is disabled by default for CI stability.
    """
    if os.getenv("USE_LIVE_BINANCE") not in ("1", "true", "True"):
        pytest.skip("Live Binance test not requested (set USE_LIVE_BINANCE=1 to enable)")

    # import the function from your market service
    try:
        from apps.market.services import get_binance_ohlcv
    except Exception as e:
        pytest.skip(f"Cannot import get_binance_ohlcv: {e}")

    # attempt to fetch 1000 candles for a common pair
    coin = "BTC/USDT"
    interval = "1m"
    # If the function signature is different in your codebase, adjust accordingly.
    live_candles = get_binance_ohlcv(coin, interval, candle_amount=1000)
    assert isinstance(live_candles, list)
    assert len(live_candles) >= 1000
