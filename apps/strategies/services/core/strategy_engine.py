import pandas as pd
from apps.strategies.services.base.base_strategy import BaseStrategy
from apps.strategies.services.base.base_indicator import BaseIndicator
from apps.strategies.services.base.base_prediction_model import BasePredictionModel
from apps.strategies.services.core.trade_risk_model import TradeRiskModel

class StrategyEngine(BaseStrategy):
    def __init__(self, strategies: list[BaseStrategy], trade_risk_model: TradeRiskModel):
        pass

    def add_strategy(self, strategy: BaseStrategy) -> None:
        pass

    def add_condition(self, indicator_list: dict[BaseIndicator], prediction_model_list: dict[BasePredictionModel], do_action_if_buy: bool = 1, do_action_if_sell: bool = 1) -> None:
        pass

    def get_signal_from_coin(self, coin: str, interval: str) -> str:
        pass

    def get_signal_from_candles(self, candles: list[dict[str, float]] | pd.DataFrame) -> str:
        pass

    def _read_strategies_from_json(self, json_data: dict) -> list[BaseStrategy]:
        pass