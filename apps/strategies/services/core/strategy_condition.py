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
        All indicators and models must signal the same action to trigger a buy or sell.
        
        Args:
            indicator_list (dict[BaseStrategy]): A dictionary of indicators used in the condition, e.g. SMAStrategy, RSIStrategy, ..etc.
            prediction_model_list (dict[BaseStrategy]): A dictionary of predictions models used in the condition.
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

        if self.do_action_if_buy:
            if not self.buy_risk_model:
                raise ValueError("Buy risk model must be provided if do_action_if_buy is True.")
            
            signals = [src.get_signal_from_candles(candles) for src in signal_sources]

            if(any(signal == 'NOT ENOUGH DATA' for signal in signals)):     #Better solution: implement ErrorMessage class and return specific details of what failed for enhanced user experience
                failed_number += 1
                
            if(all(signal == 'BUY' for signal in signals)):
                return 'BUY'
        
        if self.do_action_if_sell:
            if not self.sell_risk_model:
                raise ValueError("Sell risk model must be provided if do_action_if_sell is True.")
            
            signals = [src.get_signal_from_candles(candles) for src in signal_sources]

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
        for ind in self.strategy_list:
            if isinstance(ind, IndicatorStrategy):
                indicators.append(ind)

        models: list[PredictionModelStrategy] = []
        for model in self.strategy_list:
            if isinstance(model, PredictionModelStrategy):
                models.append(model)

        return {
                "signal models": {
                    "indicators": [ind.get_json() for ind in indicators],
                    "prediction_models": [model.get_json() for model in models]
                },
                "action": {
                    "buy_signal": self.buy_risk_model.get_json() if self.buy_risk_model else None,
                    "short_signal": self.sell_risk_model.get_json() if self.sell_risk_model else None
                }
            }
                