from apps.backtests.services.trade_engine import TradeEngine
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.strategies.services.core.strategy_engine import StrategyEngine

class BacktestEngine():
    #Finish implementing backtest class
    
    def __init__(self, strategy: StrategyEngine, trade_risk_model: TradeRiskModel | None = None, candles: list[dict] | None = None, initial_balance: float = 1000):
        self.strategy = strategy

        if trade_risk_model is None:
            self.trade_risk_model = TradeRiskModel()
        else: self.trade_risk_model = trade_risk_model

        candles = candles or []

        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.trades = []

    def set_data(self, coin: str, interval: str, candle_amount: int = 20):
        from apps.market.services import get_binance_ohlcv
        self.candles = get_binance_ohlcv(coin, interval, limit=candle_amount)

    def run(self):
        for i in range(len(self.candles)):
            current_candles = self.candles[:i+1]
            signal = self.strategy.get_signal_from_candles(current_candles)
            if signal != 'HOLD':
                # Get stop loss and take profit from risk model
                stop_loss = self.trade_risk_model.get_stop_loss()
                take_profit = self.trade_risk_model.get_take_profit() #TODO: make take_profit dynamic based on strategy calling "CLOSE" and not only the risk model

                # Create and execute trade
                trade = TradeEngine(candles=current_candles, stop_loss_pct=stop_loss, take_profit_pct=take_profit, quantity=1000, trade_type=(signal == 'BUY'))
                trade.execute()
                self.trades.append(trade)

                # Update balance based on trade result
                result = trade.get_result()
                if result != -1:
                    self.current_balance += result

        return self.current_balance, self.trades