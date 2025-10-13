import pytest  # type: ignore
from math import isclose
from backtests.services.trade_engine import Trade

def test_buy_trade_take_profit_hit():
    """Buy trade should close when take profit is reached."""
    candles = [
        {"open": 100, "high": 101, "low": 99, "close": 100.5},  # entry
        {"open": 100.5, "high": 106, "low": 100, "close": 105},  # TP hit at 105
    ]
    trade = Trade(candles, stop_loss=5, take_profit=5, quantity=1000, trade_type=True)
    trade.execute()

    assert trade.status is True or trade.exit_price != 0  # sanity
    assert trade.exit_price == pytest.approx(105)  # take profit
    assert isclose(trade.get_result(), (105 / 100) * 1000)

def test_buy_trade_stop_loss_hit():
    """Buy trade should close when stop loss is hit."""
    candles = [
        {"open": 100, "high": 101, "low": 99, "close": 100.5},
        {"open": 100.5, "high": 100.8, "low": 94.8, "close": 95},  # SL hit at 95
    ]
    trade = Trade(candles, stop_loss=5, take_profit=5, quantity=1000, trade_type=True)
    trade.execute()

    assert trade.exit_price == pytest.approx(95)
    assert isclose(trade.get_result(), (95 / 100) * 1000)

def test_sell_trade_take_profit_hit():
    """Sell trade should close when price drops enough to hit take profit."""
    # Force trade_type to sell by setting take_profit below entry
    candles = [
        {"open": 100, "high": 101, "low": 99, "close": 100.5},  # entry
        {"open": 100.5, "high": 100.8, "low": 94.8, "close": 95},  # TP hit (for sell)
    ]
    trade = Trade(candles, stop_loss=5, take_profit=5, quantity=1000, trade_type=False)
    trade.execute()

    assert trade.trade_type is False  # Confirm it's a sell
    assert trade.stop_loss == pytest.approx(105)
    assert trade.take_profit == pytest.approx(95)
    assert trade.exit_price == pytest.approx(95)
    assert isclose(trade.get_result(), (100 / 95) * 1000)

def test_sell_trade_stop_loss_hit():
    """Sell trade should close when price rises enough to hit stop loss."""
    candles = [
        {"open": 100, "high": 101, "low": 99, "close": 100.5},
        {"open": 100.5, "high": 106, "low": 100.3, "close": 105},  # SL hit (for sell)
    ]
    trade = Trade(candles, stop_loss=5, take_profit=5, quantity=1000, trade_type=False)
    trade.execute()

    assert trade.exit_price == pytest.approx(105)
    assert isclose(trade.get_result(), (100 / 105) * 1000)

def test_trade_not_closed_returns_minus_one():
    """get_result() should return -1 if trade not closed yet."""
    candles = [
        {"open": 100, "high": 102, "low": 99, "close": 101},
        {"open": 101, "high": 102, "low": 100, "close": 101.5},
    ]
    trade = Trade(candles, stop_loss=5, take_profit=5, quantity=1000, trade_type=True)
    # deliberately NOT calling execute()
    assert trade.get_result() == -1

def test_no_trigger_in_execute():
    """Trade remains open if neither TP nor SL is hit."""
    candles = [
        {"open": 100, "high": 101, "low": 99, "close": 100.5},
        {"open": 100.5, "high": 101, "low": 99.5, "close": 100.6},
    ]
    trade = Trade(candles, stop_loss=5, take_profit=5, quantity=1000, trade_type=True)
    trade.execute()

    assert trade.exit_price == 0
    assert trade.get_result() == -1  # still open