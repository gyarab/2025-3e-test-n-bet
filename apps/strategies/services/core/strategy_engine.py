from typing import Union
import pandas as pd
from apps.strategies.services.base.base_strategy import BaseStrategy
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.market.services import get_binance_ohlcv
from apps.strategies.services.base.atomic_strategy import AtomicStrategy
from apps.strategies.services.core.strategy_condition import StrategyCondition

class StrategyEngine(BaseStrategy):
    def __init__(self, conditions: list[StrategyCondition], trade_risk_model: TradeRiskModel):
        self.conditions = conditions
        self.trade_risk_model = trade_risk_model

    def add_strategy(self, strategy: AtomicStrategy, 
                     buy_risk_model: TradeRiskModel = None, 
                     sell_risk_model: TradeRiskModel = None, 
                     do_action_if_buy: bool = 1, 
                     do_action_if_sell: bool = 1) -> None:
        
        if strategy:
            condition = StrategyCondition(strategy_list=list[strategy], 
                                          buy_risk_model=buy_risk_model, 
                                          sell_risk_model=sell_risk_model, 
                                          do_action_if_buy=do_action_if_buy, 
                                          do_action_if_sell=do_action_if_sell)
            self.conditions.append(condition)

    def add_condition(self, condition: StrategyCondition) -> None:
        if condition:
            self.conditions.append(condition)

    def get_signal_from_coin(self, coin: str, interval: str, candle_amount: int = 100) -> str:
        candles = get_binance_ohlcv(coin, interval, candle_amount=candle_amount)
        return self.get_signal_from_candles(candles=candles)

    def get_signal_from_candles(self, candles: list[dict[str, float]] | pd.DataFrame) -> tuple[str, TradeRiskModel]:
        for condition in self.conditions:
            result = condition.evaluate(candles=candles)
            if result == 'BUY':
                return result, condition.buy_risk_model
            elif result == 'SELL':
                return result, condition.sell_risk_model
            
        return 'HOLD', None
    
    def get_json(self) -> dict:
        return {
            "conditions": [
                c.get_json() for c in self.conditions
            ]
        }

    @classmethod
    def _from_json(cls, json_data: dict) -> 'StrategyEngine':
        # Implement to reconstruct StrategyEngine from JSON data with conditions and risk models
        pass

