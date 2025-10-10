def generate_strategy_rules_json(indicators, models) -> dict:
    rules = {
        "conditions": [
            {
                "indicators": {
                    "RSI": {
                        "period": 14,
                        "overbought": 70,
                        "oversold": 30
                    },
                    "SMA": {
                        "short_window": 50,
                        "long_window": 200
                    }
                },
                "models": {
                    "ARIMA": "LONG"
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

