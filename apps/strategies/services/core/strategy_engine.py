from typing import Union
import pandas as pd
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.market.services import get_binance_ohlcv
from apps.strategies.services.base.atomic_strategy import AtomicStrategy
from apps.strategies.services.core.strategy_condition import StrategyCondition


class StrategyEngine():
    """
    A trading strategy engine that evaluates multiple conditions to generate buy/sell signals.
    The engine processes a list of StrategyCondition instances, where each condition is composed of at least on atomic strategy. 
    The engine evaluates each condition against the provided market data (candles) and generates a signal based on the combined output of the atomic strategies within each condition.
    """
    def __init__(self, conditions: list[StrategyCondition]):
        self.conditions = conditions

    def add_strategy(
        self,
        strategy: AtomicStrategy,
        buy_risk_model: TradeRiskModel = None,
        sell_risk_model: TradeRiskModel = None,
    ) -> None:
        if strategy:
            condition = StrategyCondition(
                strategy_list=list[strategy],
                buy_risk_model=buy_risk_model,
                sell_risk_model=sell_risk_model,
            )
            self.conditions.append(condition)

    def add_condition(self, condition: StrategyCondition) -> None:
        if condition:
            self.conditions.append(condition)


    def get_signal_and_risk_model_from_candles(
        self, candles: list[dict[str, float]] | pd.DataFrame
    ) -> tuple[str, TradeRiskModel]:
        """
        Evaluate the strategy conditions based on the provided candles and return the generated signal along with the associated risk model.
        If multiple conditions signal a buy or sell, the first one in the list will be returned. If no conditions signal a buy or sell, 'HOLD' will be returned.

        Args:
            candles (list[dict] | pd.DataFrame): OHLCV candles data to evaluate against the strategy conditions.

        Returns:
            tuple[str, TradeRiskModel]: A tuple containing the generated signal ('BUY', 'SELL', or 'HOLD') and the associated TradeRiskModel for the triggered action (or None if 'HOLD').
        """

        for condition in self.conditions:
            result = condition.evaluate(candles=candles)
            if result == "BUY":
                return (result, condition.get_trade_risk_model("BUY"))
            elif result == "SELL":
                return (result, condition.get_trade_risk_model("SELL"))

        return "HOLD", None


    def get_json(self) -> dict:
        return {"conditions": [c.get_json() for c in self.conditions]}
    

    @classmethod
    def _from_json(cls, json: dict) -> "StrategyEngine":
        """
        Create a StrategyEngine instance from JSON data.
        Expected json data structure: 
        {[
            "signal_models": {
                "indicators": [ ... ],
                "prediction_models": [ ... ]
            },
            "action": {
                "buy_signal": { ... },
                "short_signal": { ... }
            }
        ], ...}
        """
        conditions = [
            StrategyCondition._from_json(condition) for condition in json
        ]
        return cls(conditions=conditions)
