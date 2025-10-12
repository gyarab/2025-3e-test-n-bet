from strategies.services.base_strategy import BaseStrategy
from strategies.services.trade_risk_model import TradeRiskModel

class Strategy():
    def __init__(self, strategies: list[BaseStrategy], trade_risk_model: TradeRiskModel):
        pass

    def add_strategy(self, strategy: BaseStrategy) -> None:
        pass



    def _read_strategies_from_json(self, json_data: dict) -> list[BaseStrategy]:
        pass