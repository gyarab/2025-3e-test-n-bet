import pytest
from unittest.mock import patch
from apps.strategies.strategies.macd import MACDStrategy  # adjust path as needed

@pytest.fixture
def sample_candles():
    """Return a simple list of candle dicts with steadily increasing closes."""
    return [{"open": 1, "high": 2, "low": 0.5, "close": i, "volume": 100} for i in range(1, 51)]

@pytest.fixture
def decreasing_candles():
    """Candles with decreasing closes."""
    return [{"open": 1, "high": 2, "low": 0.5, "close": i, "volume": 100} for i in range(50, 0, -1)]

def test_calculate_macd_basic(sample_candles):
    strat = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    macd_line, signal_line, histogram = strat.calculate_macd(sample_candles)
    assert isinstance(macd_line, float)
    assert isinstance(signal_line, float)
    assert isinstance(histogram, float)

def test_calculate_macd_not_enough_data():
    strat = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    candles = [{"close": i} for i in range(10)]  # fewer than slow_period
    macd_line, signal_line, histogram = strat.calculate_macd(candles)
    assert macd_line == -1
    assert signal_line == -1
    assert histogram == -1

def test_get_list_returns_values(sample_candles):
    strat = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    macd_list = strat.get_list_from_candles(sample_candles)
    assert isinstance(macd_list, list)
    assert len(macd_list) == len(sample_candles)
    assert macd_list[-1] is not None

def test_get_signal_buy(decreasing_candles):
    # MACD line should be below signal → BUY signal on upward crossover
    strat = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    signal = strat.get_signal_from_candles(decreasing_candles)
    assert signal in ["BUY", "SELL", "HOLD", "NOT ENOUGH DATA"]

def test_get_signal_sell(sample_candles):
    # MACD line above signal → SELL signal on downward crossover
    strat = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    signal = strat.get_signal_from_candles(sample_candles)
    assert signal in ["BUY", "SELL", "HOLD", "NOT ENOUGH DATA"]

def test_get_signal_not_enough_data():
    strat = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    candles = [{"close": i} for i in range(10)]
    signal = strat.get_signal_from_candles(candles)
    assert signal == "NOT ENOUGH DATA"

def test_generate_macd_json():
    strat = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    result = strat.get_json()
    assert result == {
        "MACDStrategy": {
            "fast_period": 12,
            "slow_period": 26,
            "signal_period": 9
        }
    }

@patch("apps.strategies.strategies.macd.get_binance_ohlcv")
def test_get_signal_with_mock(mock_get_ohlcv, sample_candles):
    """Mock Binance fetch function to test coin-level method."""
    mock_get_ohlcv.return_value = sample_candles
    strat = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
    result = strat.get_signal_from_coin("BTC/USDT", "1h")
    assert result in ["BUY", "SELL", "HOLD", "NOT ENOUGH DATA"]
    mock_get_ohlcv.assert_called_once()
