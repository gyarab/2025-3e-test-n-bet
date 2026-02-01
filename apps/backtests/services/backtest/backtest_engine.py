from apps.backtests.services.backtest.trade_engine import TradeEngine
from apps.strategies.services.core.trade_risk_model import TradeRiskModel
from apps.strategies.services.core.strategy_engine import StrategyEngine


class BacktestEngine():
    """
    Core backtesting engine that simulates trading strategy execution on historical data.
    
    This class orchestrates the backtesting process by:
    - Loading historical market data (OHLCV candles)
    - Applying trading strategies to generate signals
    - Executing virtual trades based on signals
    - Managing risk through stop-loss and take-profit levels
    - Tracking performance and calculating results
    
    Attributes:
        strategy (StrategyEngine): The trading strategy to backtest
        trade_risk_model (TradeRiskModel): Risk management model for position sizing
        candles (list[dict]): Historical OHLCV data for backtesting
        initial_balance (float): Starting capital for the backtest
        current_balance (float): Current capital after all executed trades
        trades (list[TradeEngine]): List of all executed trades
        previous_signal (str): Last signal generated to prevent duplicate trades
    """
    
    def __init__(self, strategy: StrategyEngine, 
                 trade_risk_model: TradeRiskModel | None = None, 
                 candles: list[dict] | None = None, 
                 initial_balance: float = 1000, 
                 token: str = 'BTCUSDT', 
                 timeframe: str = '1h', 
                 candle_amount: int = 500):
        """
        Initialize the backtest engine with strategy and market data.
        
        Args:
            strategy: Trading strategy engine to use for signal generation
            trade_risk_model: Optional risk management model. If None, uses default.
            candles: Optional pre-loaded OHLCV data. If None, fetches from API.
            initial_balance: Starting capital for the backtest (default: 1000)
            token: Trading pair symbol (default: 'BTCUSDT')
            timeframe: Candle timeframe (default: '1h')
            candle_amount: Number of candles to fetch if not provided (default: 500)
        """
        self.strategy = strategy

        if trade_risk_model is None:
            self.trade_risk_model = TradeRiskModel()
        else:
            self.trade_risk_model = trade_risk_model

        # Load candles from provided data or fetch from market
        self.candles = candles or self.set_data(token, timeframe, candle_amount)

        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.trades = []
        self.previous_signal = 'HOLD'

    def set_data(self, coin: str, interval: str, candle_amount: int = 20):
        """
        Fetch historical market data from Binance.
        
        Args:
            coin: Trading pair symbol (e.g., 'BTCUSDT')
            interval: Timeframe for candles (e.g., '1h', '4h', '1d')
            candle_amount: Number of candles to fetch (default: 20)
            
        Returns:
            list[dict]: List of OHLCV candle dictionaries
        """
        from apps.market.services import get_binance_ohlcv
        return get_binance_ohlcv(coin, interval, limit=candle_amount)

    def run(self):
        """
        Execute the backtest by iterating through historical data.
        
        For each candle:
        1. Generate trading signal from strategy
        2. Execute trade if signal changes from previous
        3. Apply risk management (stop-loss, take-profit)
        4. Update balance based on trade results
        
        Returns:
            tuple: (final_balance, list_of_trades)
                - final_balance (float): Ending capital after all trades
                - list_of_trades (list[TradeEngine]): All executed trades
        """
        for i in range(len(self.candles)):
            # Provide strategy with candles up to current point
            current_candles = self.candles[:i+1]
            signal = self.strategy.get_signal_from_candles(current_candles)

            # Handle tuple return values from some strategies
            if isinstance(signal, tuple):
                signal = signal[0]

            # TODO: prevent multiple opposite trades in the same moment
            # (Need to open new trade only after previous is closed)

            # Only trade when signal changes from previous state
            if signal != 'HOLD' and signal != self.previous_signal:
                # Get stop loss and take profit from risk model
                stop_loss = self.trade_risk_model.get_stop_loss()
                # TODO: make take_profit dynamic based on strategy calling
                # "CLOSE" and not only the risk model
                take_profit = self.trade_risk_model.get_take_profit()

                # Calculate position quantity
                quantity = self.trade_risk_model.get_position_quantity(
                    self.current_balance
                )

                # Create and execute trade
                trade = TradeEngine(
                    candles=self.candles[i:],
                    stop_loss_pct=stop_loss,
                    take_profit_pct=take_profit,
                    quantity=quantity,
                    trade_type=(signal == 'BUY')
                )
                trade.execute()
                self.trades.append(trade)
                self.previous_signal = signal

                # Update balance based on trade result
                result = trade.get_result()
                if result is not None:
                    self.current_balance += result

        return self.current_balance, self.trades