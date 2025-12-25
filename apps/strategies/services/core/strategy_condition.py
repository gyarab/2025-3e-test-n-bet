import pandas as pd
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.strategies.services.base.atomic_strategy import AtomicStrategy
from apps.strategies.services.base.indicator_strategy import IndicatorStrategy
from apps.strategies.services.base.prediction_model_strategy import PredictionModelStrategy


class StrategyCondition():
    def __init__(self, 
                 strategy_list: list[AtomicStrategy],
                 buy_risk_model: TradeRiskModel = None, 
                 sell_risk_model: TradeRiskModel = None, 
                 do_action_if_buy: bool = 1, 
                 do_action_if_sell: bool = 1):
        """
        A condition within a trading strategy that combines indicators and prediction models to generate buy/sell signals. 
        Condition is composed of multiple atomic strategies (indicator-based and/or prediction-model-based), but treated as a single unit with the same buy/sell risk models and logic.
        All indicators and models must signal the same action to trigger a buy or sell.
        
        Args:
            strategy_list (list[AtomicStrategy]): List of strategies (indicator-based and/or prediction-model-based) to evaluate.
            buy_risk_model (TradeRiskModel): Risk model to apply when a buy signal is generated.
            sell_risk_model (TradeRiskModel): Risk model to apply when a sell signal is generated.
            do_action_if_buy (bool): Whether to perform an action if the condition signals a buy (default True).
            do_action_if_sell (bool): Whether to perform an action if the condition signals a sell (default True).
        """
        self.strategy_list = strategy_list
        self.do_action_if_buy = do_action_if_buy
        self.do_action_if_sell = do_action_if_sell
        self.buy_risk_model = buy_risk_model or TradeRiskModel()
        self.sell_risk_model = sell_risk_model or TradeRiskModel()

    def evaluate(self, candles: list[dict[str, float]]) -> str:
        
        signal_sources = self.strategy_list

        failed_number = 0

        if not signal_sources: # No indicators or models to evaluate
            return 'HOLD'

        signals = [src.get_signal_from_candles(candles) for src in signal_sources]

        # All signals must agree to trigger an action

        if self.do_action_if_buy:
            if not self.buy_risk_model:
                raise ValueError("Buy risk model must be provided if do_action_if_buy is True.")
                   
            if(any(signal == 'NOT ENOUGH DATA' for signal in signals)):  
                failed_number += 1
                
            if(all(signal == 'BUY' for signal in signals)):
                return 'BUY'
        
        if self.do_action_if_sell:
            if not self.sell_risk_model:
                raise ValueError("Sell risk model must be provided if do_action_if_sell is True.")

            if(any(signal == 'NOT ENOUGH DATA' for signal in signals)):
                failed_number += 1

            if(all(signal == 'SELL' for signal in signals)):
                return 'SELL'
        
        return 'HOLD'
        
    def set_buy_risk_model(self, risk_model: TradeRiskModel):
        self.buy_risk_model = risk_model
    
    def set_sell_risk_model(self, risk_model: TradeRiskModel):
        self.sell_risk_model = risk_model

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
                    "prediction_models": [model.get_json() for model in models]
                },
                "risk_models": {
                    "buy_signal": self.buy_risk_model.get_json() if self.buy_risk_model else None,
                    "short_signal": self.sell_risk_model.get_json() if self.sell_risk_model else None
                }
            }
    
    @classmethod
    def _from_json(cls, json_data: dict) -> 'StrategyCondition':
        """
        Generate StrategyCondition instance from JSON data.
        Expected json data structure:
        {
            "signal_models": {
                "indicators": [ ... ],
                "prediction_models": [ ... ]
            },
            "action": {
                "buy_signal": { ... },
                "short_signal": { ... }
            },
            "do_action_if_buy": 1,
            "do_action_if_sell": 1
        }
        """
        # Load indicator strategies
        indicators_json = json_data.get("signal_models", {}).get("indicators", [])
        indicators = [IndicatorStrategy._from_json(ind_json) for ind_json in indicators_json]

        # Load prediction model strategies
        models_json = json_data.get("signal_models", {}).get("prediction_models", [])
        models = [PredictionModelStrategy._from_json(model_json) for model_json in models_json]

        strategy_list = indicators + models

        # Load risk models
        buy_risk_model_json = json_data.get("action", {}).get("buy_signal", None)
        buy_risk_model = TradeRiskModel._from_json(buy_risk_model_json) if buy_risk_model_json else TradeRiskModel()

        sell_risk_model_json = json_data.get("action", {}).get("short_signal", None)
        sell_risk_model = TradeRiskModel._from_json(sell_risk_model_json) if sell_risk_model_json else TradeRiskModel()

        return cls(
            strategy_list=strategy_list,
            buy_risk_model=buy_risk_model,
            sell_risk_model=sell_risk_model,
            do_action_if_buy=json_data.get("do_action_if_buy", 1),
            do_action_if_sell=json_data.get("do_action_if_sell", 1)
        )
                