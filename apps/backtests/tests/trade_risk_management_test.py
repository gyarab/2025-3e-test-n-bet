import pytest # type: ignore
from math import isclose
from apps.strategies.services.core.trade_risk_model import TradeRiskModel 


@pytest.fixture
def sample_candles():
    """Generate fake OHLC candles for ATR-based tests."""
    return [
        {"high": 102 + i, "low": 98 + i, "close": 100 + i}
        for i in range(20)
    ]


def test_fixed_stop_loss_and_take_profit_initialization():
    """Test initialization with fixed stop-loss and take-profit."""
    trade = TradeRiskModel(stop_loss_pct=5, take_profit_pct=10)

    # ensure correct setup
    assert trade.stop_loss_pct == 5
    assert trade.take_profit_pct == 10
    assert trade.get_stop_loss() == 5
    assert trade.get_take_profit() == 10


def test_set_stop_loss_fixed():
    trade = TradeRiskModel(stop_loss_pct=3)
    result = trade.set_stop_loss(stop_loss_type='fixed', stop_loss_pct=3)
    assert result == 3
    assert trade.stop_loss_type == 'fixed'
    assert trade.stop_loss_pct == 3


def test_set_take_profit_fixed():
    trade = TradeRiskModel(stop_loss_pct=5, take_profit_pct=10)
    result = trade.set_take_profit(take_profit_type='fixed', take_profit_pct=12)
    assert result == trade.stop_loss_pct  # returns stop_loss_pct
    assert trade.take_profit_pct == 12
    assert trade.take_profit_type == 'fixed'


def test_calculate_stop_loss_price_valid():
    price = TradeRiskModel.calculate_stop_loss_price(100, 100, 0.05)
    assert price == 95.00


def test_calculate_take_profit_price_valid():
    price = TradeRiskModel.calculate_take_profit_price(100, 100, 0.10)
    assert price == 110.00


def test_calculate_stop_loss_price_invalid():
    with pytest.raises(ValueError):
        TradeRiskModel.calculate_stop_loss_price(0, 100, 0.05)
    with pytest.raises(ValueError):
        TradeRiskModel.calculate_stop_loss_price(100, 100, 0)


def test_calculate_take_profit_price_invalid():
    with pytest.raises(ValueError):
        TradeRiskModel.calculate_take_profit_price(-10, 100, 0.1)


def test_relative_stop_loss_percentage(sample_candles):
    """Test that relative stop loss returns a reasonable % value."""
    result = TradeRiskModel._calculate_relative_stop_loss_percentage(sample_candles, period=14, atr_multiplier=1.5)
    # ATR-based % should be positive and small
    assert result > 0
    assert result < 10


def test_relative_stop_loss_raises_for_few_candles():
    with pytest.raises(ValueError):
        TradeRiskModel._calculate_relative_stop_loss_percentage(
            [{"high": 101, "low": 99, "close": 100}], period=14
        )


def test_relative_take_profit_based_on_stop_loss(sample_candles):
    """Ensure relative take-profit uses stop-loss * multiplier."""
    trade = TradeRiskModel(stop_loss_pct=5)
    trade.stop_loss_type = 'relative'
    trade.stop_loss_pct = 3
    result = trade.set_take_profit(take_profit_type='relative', multiplier=2)
    assert isclose(trade.take_profit_pct, 6.0)
    assert trade.take_profit_type == 'relative'
    assert result == trade.stop_loss_pct


def test_invalid_stop_loss_type():
    trade = TradeRiskModel(stop_loss_pct=5)
    trade.stop_loss_type = 'invalid_type'
    with pytest.raises(ValueError):
        trade.set_stop_loss(stop_loss_type='invalid')


def test_invalid_take_profit_type():
    trade = TradeRiskModel(stop_loss_pct=5)
    trade.stop_loss_type = 'invalid_type'
    with pytest.raises(ValueError):
        trade.set_take_profit(take_profit_type='invalid')
