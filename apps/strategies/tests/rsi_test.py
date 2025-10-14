import pytest # type: ignore
import pandas as pd
from unittest.mock import patch

from apps.strategies.services.strategies.rsi_strategy import RSIStrategy  # adjust path as needed


@pytest.fixture
def sample_candles():
    """Return a simple list of candle dicts with close prices increasing."""
    return [{"open": 1, "high": 2, "low": 0.5, "close": i, "volume": 100} for i in range(1, 51)]


def test_calculate_rsi_basic(sample_candles):
    strat = RSIStrategy()
    rsi = strat.indicator().calculate(sample_candles)
    # steadily increasing closes → RSI should be 100
    assert round(rsi, 3) == 100.0


def test_calculate_rsi_not_enough_data():
    strat = RSIStrategy.from_parametrs(period=60)  # period longer than candle length
    candles = [{"close": i} for i in range(10)]
    assert strat.indicator().calculate(candles) == -1


def test_get_list_returns_values(sample_candles):
    strat = RSIStrategy.from_parametrs(period = 10)
    rsi_list = strat.indicator().get_list_from_candles(sample_candles)
    assert isinstance(rsi_list, list)
    assert len(rsi_list) == len(sample_candles)
    # First few should be None due to insufficient data
    assert all(x is None for x in rsi_list[:4])
    assert rsi_list[-1] is not None


def test_get_signal_buy():
    # decreasing prices → RSI < oversold → BUY
    candles = [{"open": 1, "high": 2, "low": 0.5, "close": i, "volume": 100} for i in range(100, 50, -1)]
    strat = RSIStrategy.from_parametrs(period=14, oversold=30, overbought=70)
    signal = strat.get_signal_from_candles(candles)
    assert signal == "BUY"


def test_get_signal_sell():
    # increasing prices → RSI > overbought → SELL
    candles = [{"open": 1, "high": 2, "low": 0.5, "close": i, "volume": 100} for i in range(1, 51)]
    strat = RSIStrategy.from_parametrs(period=14, oversold=30, overbought=70)
    signal = strat.get_signal_from_candles(candles)
    assert signal == "SELL"


def test_get_signal_not_enough_data():
    strat = RSIStrategy.from_parametrs(period = 14, oversold = 30, overbought = 70)
    candles = [{"close": i} for i in range(10)]
    assert strat.get_signal_from_candles(candles) == "NOT ENOUGH DATA"


def test_generate_rsi_json():
    strat = RSIStrategy.from_parametrs(period = 18, oversold = 20, overbought = 50)
    result = strat.get_json()
    assert result == {"RSIStrategy": {
                "period": 18,
                "oversold": 20,
                "overbought": 50
            }}


@patch("apps.strategies.services.strategies.rsi_strategy.get_binance_ohlcv")
def test_get_signal_with_mock(mock_get_ohlcv, sample_candles):
    """Mock Binance fetch function to ensure integration behavior works."""
    mock_get_ohlcv.return_value = sample_candles
    strat = RSIStrategy.from_parametrs(period = 14, oversold = 30, overbought = 70)
    
    # call the correct method
    result = strat.get_signal_from_coin("BTC/USDT", "1h")
    
    # should return a valid signal string
    assert result in ["BUY", "SELL", "HOLD", "NOT ENOUGH DATA"]
    
    mock_get_ohlcv.assert_called_once()
