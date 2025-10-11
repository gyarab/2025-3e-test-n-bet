from apps.strategies.services.base_strategy import BaseStrategy

class Backtest():
    #Finish implementing backtest class
    
    def __init__(self, strategy: BaseStrategy, candles: list[dict], initial_balance: float = 1000):
        self.strategy = strategy
        self.candles = candles
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.trades = []

    def run(self):
        for i in range(len(self.candles)):
            current_candles = self.candles[:i+1]
            signal = self.strategy.get_signal_from_candles(current_candles)
            # Implement trade execution logic based on the signal
            # Update current_balance and trades list accordingly
        return self.current_balance, self.trades