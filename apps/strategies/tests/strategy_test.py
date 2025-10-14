import pytest # type: ignore
from unittest.mock import MagicMock
from apps.strategies.services.base.atomic_strategy import AtomicStrategy
from apps.strategies.services.base.indicator_strategy import IndicatorStrategy
from apps.strategies.services.base.prediction_model_strategy import PredictionModelStrategy
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.strategies.services.core.strategy_condition import StrategyCondition
from apps.strategies.services.core.strategy_engine import StrategyEngine


# ----------------------------
# Fixtures
# ----------------------------
@pytest.fixture
def mock_indicator():
    ind = MagicMock(spec=IndicatorStrategy)
    ind.get_signal_from_candles.return_value = 'BUY'
    ind.get_json.return_value = {"MockIndicator": {"param": 1}}
    return ind

@pytest.fixture
def mock_model():
    model = MagicMock(spec=PredictionModelStrategy)
    model.get_signal_from_candles.return_value = 'SELL'
    model.get_json.return_value = {"MockModel": {"param": 2}}
    return model

@pytest.fixture
def mock_candles():
    return [{"open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 100}] * 10


# ----------------------------
# Tests for StrategyCondition
# ----------------------------
def test_strategy_condition_buy_signal(mock_indicator, mock_candles):
    condition = StrategyCondition(strategy_list=[mock_indicator])
    result = condition.evaluate(mock_candles)
    assert result == 'BUY'
    json_output = condition.get_json()
    assert "signal models" in json_output
    assert json_output["signal models"]["indicators"][0] == {"MockIndicator": {"param": 1}}
    assert json_output["action"]["buy_signal"] is not None


def test_strategy_condition_sell_signal(mock_model, mock_candles):
    condition = StrategyCondition(strategy_list=[mock_model])
    result = condition.evaluate(mock_candles)
    assert result == 'SELL'
    json_output = condition.get_json()
    assert "signal models" in json_output
    assert json_output["signal models"]["prediction_models"][0] == {"MockModel": {"param": 2}}
    assert json_output["action"]["short_signal"] is not None


def test_strategy_condition_hold_signal(mock_indicator, mock_model, mock_candles):
    # Mix of BUY and SELL should produce HOLD
    condition = StrategyCondition(strategy_list=[mock_indicator, mock_model])
    result = condition.evaluate(mock_candles)
    assert result == 'HOLD'


# ----------------------------
# Tests for StrategyEngine
# ----------------------------
def test_strategy_engine_signal(mock_indicator, mock_model, mock_candles):
    buy_condition = StrategyCondition(strategy_list=[mock_indicator])
    sell_condition = StrategyCondition(strategy_list=[mock_model])
    engine = StrategyEngine(conditions=[buy_condition, sell_condition], trade_risk_model=TradeRiskModel())
    
    # Engine should return the first matched signal
    signal, risk_model = engine.get_signal_from_candles(mock_candles)
    assert signal in ('BUY', 'SELL', 'HOLD')
    if signal == 'BUY':
        assert risk_model == buy_condition.buy_risk_model
    elif signal == 'SELL':
        assert risk_model == sell_condition.sell_risk_model
    else:
        assert risk_model is None


def test_strategy_engine_json(mock_indicator, mock_model):
    condition1 = StrategyCondition(strategy_list=[mock_indicator])
    condition2 = StrategyCondition(strategy_list=[mock_model])
    engine = StrategyEngine(conditions=[condition1, condition2], trade_risk_model=TradeRiskModel())
    json_output = engine.get_json()
    
    assert "conditions" in json_output
    assert len(json_output["conditions"]) == 2
    assert "signal models" in json_output["conditions"][0]
    assert "signal models" in json_output["conditions"][1]
