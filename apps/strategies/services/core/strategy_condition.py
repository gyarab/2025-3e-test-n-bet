import pandas as pd
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.strategies.services.base.atomic_strategy import AtomicStrategy
from apps.strategies.services.base.indicator_strategy import IndicatorStrategy
from apps.strategies.services.base.prediction_model_strategy import (
    PredictionModelStrategy,
)


class StrategyCondition:
    def __init__(
        self,
        strategy_list: list[AtomicStrategy],
        buy_risk_model: TradeRiskModel = None,
        sell_risk_model: TradeRiskModel = None
    ):
        """
        A condition within a trading strategy that combines indicators and prediction models to generate buy/sell signals.
        Condition is composed of multiple atomic strategies (indicator-based and/or prediction-model-based), but treated as a single unit with the same buy/sell risk models and logic.
        All indicators and models must signal the same action to trigger a buy or sell.

        Args:
            strategy_list (list[AtomicStrategy]): List of atomic strategies (indicator-based and/or prediction-model-based) to evaluate.
            buy_risk_model (TradeRiskModel): Risk model to apply when a buy signal is generated.
            sell_risk_model (TradeRiskModel): Risk model to apply when a sell signal is generated.
        """
        self.strategy_list = strategy_list
        self.buy_risk_model = buy_risk_model or TradeRiskModel()
        self.sell_risk_model = sell_risk_model or TradeRiskModel()

    def evaluate(self, candles: list[dict[str, float]]) -> str:

        signal_sources = self.strategy_list

        if not signal_sources:  # No indicators or models to evaluate
            return "HOLD"

        signals = [src.get_signal_from_candles(candles) for src in signal_sources]

        # All signals must agree to trigger an action

        if all(signal == "BUY" for signal in signals):
            return "BUY"
        
        if all(signal == "SELL" for signal in signals):
            return "SELL"

        return "HOLD"
    
    def get_trade_risk_model(self, signal_type: str) -> TradeRiskModel:
        """
        Get the appropriate TradeRiskModel based on the signal type.

        Args:
            signal_type (str): The type of signal ('BUY' or 'SELL').
            
        Returns:
            TradeRiskModel: The corresponding risk model for the signal type.
        """
        if signal_type == "BUY":
            return self.buy_risk_model
        elif signal_type == "SELL":
            return self.sell_risk_model
        else:
            raise ValueError("Invalid signal type. Must be 'BUY' or 'SELL'.")

    def get_json(self) -> dict:
        indicators: list[IndicatorStrategy] = []

        # Collect only indicator-based strategies
        for ind in self.strategy_list:
            if isinstance(ind, IndicatorStrategy):
                indicators.append(ind)

        # Collect only prediction model-based strategies
        models: list[PredictionModelStrategy] = []
        for model in self.strategy_list:
            if isinstance(model, PredictionModelStrategy):
                models.append(model)

        return {
            "signal_models": {
                "indicators": [ind.get_json() for ind in indicators],
                "prediction_models": [model.get_json() for model in models],
            },
            "risk_models": {
                "buy_signal": (
                    self.buy_risk_model.get_json() if self.buy_risk_model else None
                ),
                "short_signal": (
                    self.sell_risk_model.get_json() if self.sell_risk_model else None
                ),
            },
        }

    @classmethod
    def _from_json(cls, json_data: dict) -> "StrategyCondition":
        """
        Generate StrategyCondition instance from JSON data.
        Expects JSON data structure:
        {
            "signal_models": {
                "indicators": [ ... ],
                "prediction_models": [ ... ]
            },
            "action": {
                "buy_signal": { ... },
                "short_signal": { ... }
            }
        }
        """
        if not isinstance(json_data, dict):
            raise ValueError("Invalid JSON data for StrategyCondition. Expected a dictionary.")
        
        if "signal_models" not in json_data:
            raise ValueError("Missing 'signal_models' key in JSON data for StrategyCondition.")
        
        if "indicators" not in json_data["signal_models"] or "prediction_models" not in json_data["signal_models"]:
            raise ValueError("Missing 'indicators' or 'prediction_models' key in 'signal_models' of JSON data for StrategyCondition.")
        
        if "action" not in json_data:
            raise ValueError("Missing 'action' key in JSON data for StrategyCondition.")

        # Load indicator strategies
        indicators_json = json_data.get("signal_models", {}).get("indicators", [])
        indicators = [
            IndicatorStrategy._from_json(ind_json) for ind_json in indicators_json
        ]

        # Load prediction model strategies
        models_json = json_data.get("signal_models", {}).get("prediction_models", [])
        models = [
            PredictionModelStrategy._from_json(model_json) for model_json in models_json
        ]

        strategy_list = indicators + models

        # Load risk models
        buy_risk_model_json = json_data.get("action", {}).get("buy_signal", None)
        buy_risk_model = (
            TradeRiskModel._from_json(buy_risk_model_json)
            if buy_risk_model_json
            else TradeRiskModel()
        )

        sell_risk_model_json = json_data.get("action", {}).get("sell_signal", None)
        sell_risk_model = (
            TradeRiskModel._from_json(sell_risk_model_json)
            if sell_risk_model_json
            else TradeRiskModel()
        )

        return cls(
            strategy_list=strategy_list,
            buy_risk_model=buy_risk_model,
            sell_risk_model=sell_risk_model
        )
