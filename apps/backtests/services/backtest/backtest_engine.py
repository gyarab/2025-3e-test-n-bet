from apps.backtests.services.backtest.trade_engine import TradeEngine
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.strategies.services.core.strategy_engine import StrategyEngine


class BacktestEngine:
    def __init__(
        self,
        strategy: StrategyEngine,
        candles: list[dict] | None = None,
        initial_balance: float = 1000,
        token: str = "BTCUSDT",
        timeframe: str = "1h",
        candle_amount: int = 500,
    ):

        self.strategy = strategy

        # Implement function to check candles input
        self.candles = candles or self.set_data(token, timeframe, candle_amount)
        self._validate_candles(self.candles)

        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.trades = []
        self.previous_signal = "HOLD"
        self.active_trade = None

    def _validate_candles(self, candles: list[dict]):
        required_keys = {"open", "high", "low", "close", "volume", "open_time"}
        for candle in candles:
            if not required_keys.issubset(candle.keys()):
                raise ValueError(
                    f"Each candle must contain the following keys: {required_keys}"
                )

    def set_data(self, coin: str, interval: str, candle_amount: int = 20):
        from apps.market.services import get_binance_ohlcv

        return get_binance_ohlcv(coin, interval, limit=candle_amount)

    def run(self):
        if not self.candles:
            raise ValueError("No candles data provided for backtesting.")
        
        if not self.strategy:
            raise ValueError("No strategy provided for backtesting.")

        # Iterate through candles and evaluate strategy at each step.
        # TODO: open trade only when there is no open
        for i in range(len(self.candles) - 1):
            past_candles = self.candles[:i + 1]
            current_candle = self.candles[i + 1]

            signal, trade_risk_model = self.strategy.get_signal_and_risk_model_from_candles(past_candles)

            if signal != "BUY" and signal != "SELL" and signal != "HOLD":
                raise ValueError(f"Invalid signal '{signal}' returned by strategy. Expected 'BUY', 'SELL', or 'HOLD'.")
            
            if (signal == "BUY" or signal == "SELL") and trade_risk_model is None:
                raise ValueError("Trade risk model must be provided for BUY or SELL signals.")


            if self.active_trade is None and signal in ("BUY", "SELL"):
                # Get stop loss and take profit from risk model
                stop_loss = trade_risk_model.get_stop_loss(candles=past_candles)
                take_profit = (
                    trade_risk_model.get_take_profit(candles=past_candles)
                )  # TODO: make take_profit dynamic based on strategy calling "CLOSE" and not only the risk model

                # Calculate position quantity
                quantity = trade_risk_model.get_position_quantity(
                    self.current_balance, candles=past_candles
                )

                # Create and execute trade
                trade = TradeEngine(
                    open_candle=current_candle,  # Assuming we enter the trade at the open of the next candle after signal
                    stop_loss_pct=stop_loss,
                    take_profit_pct=take_profit,
                    quantity=quantity,
                    trade_type=(signal == "BUY" or signal == 1),  # Assuming signal can be "BUY"/"SELL" or 1/0
                )

                self.active_trade = trade

                '''
                # If we want to execute the whole trade immediately, and then move to the next candle.
                # This means that several trades can be opened at the same time 

                trade.execute(self.candles[i:])
                self.trades.append(trade)
                self.previous_signal = signal

                # Update balance based on trade result
                result = trade.get_result()
                if result != None:
                    if self.current_balance + result <= 0:
                        self.current_balance = 0
                        break
                    else: 
                        self.current_candles += result
                '''

            # If we want to wait for the trade to close before opening a new one, we need to update the active trade with each new candle and check if it has closed.
            if self.active_trade is not None:
                self.active_trade.update(current_candle)  # Update the active trade with the new candle
                if not self.active_trade.status:  # Trade closed
                    result = self.active_trade.get_result()
                    if result != None:
                        self.current_balance = max(0, self.current_balance + result)

                        if self.current_balance <= 0:
                            break

                    self.trades.append(self.active_trade)
                    self.active_trade = None
                

        return self.current_balance, self.trades
