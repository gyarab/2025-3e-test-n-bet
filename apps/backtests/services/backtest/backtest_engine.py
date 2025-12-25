from apps.backtests.services.backtest.trade_engine import TradeEngine
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.strategies.services.core.strategy_engine import StrategyEngine

class BacktestEngine():
    #Finish implementing backtest class
    
    def __init__(self, strategy: StrategyEngine, 
                 trade_risk_model: TradeRiskModel | None = None, 
                 candles: list[dict] | None = None, 
                 initial_balance: float = 1000, 
                 token: str = 'BTCUSDT', 
                 timeframe: str = '1h', 
                 candle_amount: int = 500):
        
        self.strategy = strategy

        if trade_risk_model is None:
            self.trade_risk_model = TradeRiskModel()
        else: self.trade_risk_model = trade_risk_model

        # Implement function to check candles input
        self.candles = candles or self.set_data(token, timeframe, candle_amount)

        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.trades = []
        self.previous_signal = 'HOLD'

    def set_data(self, coin: str, interval: str, candle_amount: int = 20):
        from apps.market.services import get_binance_ohlcv
        return get_binance_ohlcv(coin, interval, limit=candle_amount)

    def run(self):
        for i in range(len(self.candles)):
            current_candles = self.candles[:i+1]
            signal = self.strategy.get_signal_from_candles(current_candles)

            if isinstance(signal, tuple):
                signal = signal[0]

            #TODO: prevent multiple oposite trades in the same moment(Need to open new trade only after previous is closed)!

            if signal != 'HOLD' and signal != self.previous_signal:
                # Get stop loss and take profit from risk model
                stop_loss = self.trade_risk_model.get_stop_loss()
                take_profit = self.trade_risk_model.get_take_profit() #TODO: make take_profit dynamic based on strategy calling "CLOSE" and not only the risk model

                # Calculate position quantity
                quantity = self.trade_risk_model.get_position_quantity(self.current_balance)

                # Create and execute trade
                trade = TradeEngine(candles=self.candles[i:], stop_loss_pct=stop_loss, take_profit_pct=take_profit, quantity=quantity, trade_type=(signal == 'BUY'))
                trade.execute()
                self.trades.append(trade)
                self.previous_signal = signal

                # Update balance based on trade result
                result = trade.get_result()
                if result != -1:
                    self.current_balance += result

        return self.current_balance, self.trades