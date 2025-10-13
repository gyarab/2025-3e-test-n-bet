import pandas as pd
from strategies.services.base_indicator import BaseIndicator
from strategies.services.base_prediction_model import BasePredictionModel
from strategies.services.trade_risk_model import TradeRiskModel


class StrategyCondition():
    def __init__(self, 
                 indicator_list: list[BaseIndicator], 
                 prediction_model_list: list[BasePredictionModel], 
                 buy_risk_model: TradeRiskModel = None, 
                 sell_risk_model: TradeRiskModel = None, 
                 do_action_if_buy: bool = 1, 
                 do_action_if_sell: bool = 1):
        """
        A condition within a trading strategy that combines indicators and prediction models to generate buy/sell signals. 
        All indicators and models must signal the same action to trigger a buy or sell.
        
        Args:
            indicator_list (dict[BaseIndicator]): A dictionary of indicators used in the condition.
            prediction_model_list (dict[BasePredictionModel]): A dictionary of prediction models used in the condition.
            do_action_if_buy (bool): Whether to perform an action if the condition signals a buy (default True).
            do_action_if_sell (bool): Whether to perform an action if the condition signals a sell (default True).
        """
        self.indicator_list = indicator_list
        self.prediction_model_list = prediction_model_list
        self.do_action_if_buy = do_action_if_buy
        self.do_action_if_sell = do_action_if_sell
        self.buy_risk_model = buy_risk_model or TradeRiskModel()
        self.sell_risk_model = sell_risk_model or TradeRiskModel()

    def evaluate(self, candles: list[dict[str, float]]) -> str:
        if self.do_action_if_buy:
            if not self.buy_risk_model:
                raise ValueError("Buy risk model must be provided if do_action_if_buy is True.")
            
            buy_signal = 1 if all(
                indicator.get_signal(candles) == 'BUY' for indicator in self.indicator_list) and all(
                model.get_signal(candles) == 'BUY' for model in self.prediction_model_list) else 0

            #finish
        
        sell_signal = 1 if all(
            indicator.get_signal(candles) == 'SELL' for indicator in self.indicator_list) and all(
            model.get_signal(candles) == 'SELL' for model in self.prediction_model_list
            ) else 0
        
        if buy_signal and self.do_action_if_buy:
            return 'BUY'
        elif sell_signal and self.do_action_if_sell:
            return 'SELL'
            