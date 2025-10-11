from apps.strategies.services.base_strategy import BaseStrategy
from apps.strategies.services.base_model import BaseModel
from apps.strategies.services.base_indicator import BaseIndicator

def generate_strategy_rules_json(indicators: list[BaseIndicator], models: list[BaseModel]) -> dict:
    
    rules = {
        "conditions": [
            {
                "indicators": {
                    type(i).__name__: i.get_json()[type(i).__name__] #name of each strategy class, e.g. SMAStrategy, RSIStrategy, etc.
                    for i in indicators
                },
                "models": {
                    type(i).__name__: i.get_json()[type(i).__name__] #name of each strategy class, e.g. ARIMA, etc.
                    for i in models
                },
                "logic": "RSI.LONG & SMA.LONG & ARIMA.LONG",
                "action": {
                    "type": "LONG | SHORT",
                    "max_loss_size": 10,
                    "stop_loss": {
                        "type": "fixed | relevant",
                        "based_on": "24h",
                        "percentage": "5%"
                    }
                }
            }
        ]
    }
    return rules

