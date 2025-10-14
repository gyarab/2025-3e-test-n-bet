import pytest # type: ignore
import pandas as pd
from unittest.mock import patch

from apps.strategies.services.strategies.sma_strategy import SMAStrategy  # adjust path as needed


@pytest.fixture
def sample_candles():
    """Return a simple list of candle dicts with close prices increasing."""
    return [{"open": 1, "high": 2, "low": 0.5, "close": i, "volume": 100} for i in range(1, 51)]


def test_calculate_sma_basic(sample_candles):
    strat = SMAStrategy.from_parametrs(short_window=5, long_window=10)
    sma = strat.indicator().calculate(sample_candles, window=5)
    # Expected SMA = mean of last 5 closes (46–50)
    expected = sum([46,47,48,49,50]) / 5
    assert round(sma, 3) == round(expected, 3)


def test_calculate_sma_not_enough_data():
    strat = SMAStrategy.from_parametrs(short_window=5)
    candles = [{"close": i} for i in range(3)]  # fewer than window
    assert strat.indicator().calculate(candles, window=5) == -1


def test_get_list_returns_values(sample_candles):
    strat = SMAStrategy.from_parametrs(short_window=5)
    sma_list = strat.indicator().get_list_from_candles(sample_candles)
    assert isinstance(sma_list, list)
    assert len(sma_list) == len(sample_candles)
    # First few should be None due to insufficient data
    assert all(x is None for x in sma_list[:4])
    assert sma_list[-1] is not None


def test_get_signal_buy(sample_candles):
    strat = SMAStrategy.from_parametrs(short_window=5, long_window=20)
    # increasing prices -> short SMA > long SMA
    signal = strat.get_signal_from_candles(sample_candles)
    assert signal == "BUY"


def test_get_signal_sell():
    # decreasing prices -> short SMA < long SMA
    candles = [{"open": 1, "high": 2, "low": 0.5, "close": i, "volume": 100} for i in range(100, 50, -1)]
    strat = SMAStrategy.from_parametrs(short_window=5, long_window=20)
    signal = strat.get_signal_from_candles(candles)
    assert signal == "SELL"


def test_get_signal_not_enough_data():
    strat = SMAStrategy.from_parametrs(short_window=5, long_window=20)
    candles = [{"close": i} for i in range(10)]
    assert strat.get_signal_from_candles(candles) == "NOT ENOUGH DATA"


def test_generate_sma_json():
    strat = SMAStrategy.from_parametrs(short_window=7, long_window=21)
    result = strat.get_json()
    assert result == {"SMAStrategy": {"short_window": 7, "long_window": 21}}


@patch("apps.strategies.services.strategies.sma_strategy.get_binance_ohlcv")
def test_get_signal_with_mock(mock_get_ohlcv, sample_candles):
    """Mock Binance fetch function to ensure integration behavior works."""
    mock_get_ohlcv.return_value = sample_candles
    strat = SMAStrategy.from_parametrs(short_window=5, long_window=20)
    
    # call the correct method
    result = strat.get_signal_from_coin("BTC/USDT", "1h")
    
    # should return a valid signal string
    assert result in ["BUY", "SELL", "HOLD", "NOT ENOUGH DATA"]
    
    mock_get_ohlcv.assert_called_once()
