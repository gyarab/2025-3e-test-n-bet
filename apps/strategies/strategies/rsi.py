# apps/strategies/strategies/rsi.py
import pandas as pd

from apps.strategies.strategies.base_strategy import BaseStrategy
from apps.strategies.strategies.base_indicator import BaseIndicator

from apps.market.services import get_binance_ohlcv

class RSIStrategy(BaseStrategy, BaseIndicator):
    def __init__(self, period: int = 14, oversold: int = 30, overbought: int = 70):
        """
        Args:
            period (int): Period for short RSI (default 14)
            oversold (int): RSI value below which we buy (default 30)
            overbought (int): RSI value above which we sell (default 70)
        """
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def calculate_rsi(self, candles):
        """
        Calculate Relative Strength Index (RSI) for the last candle from a list of OHLCV candles.

        Args:
            candles (list[dict]): List of dictionaries, each containing: close
        Returns:
            float: Latest RSI value or -1 if not enough data
        """
        if not candles or len(candles) < self.period:
            return -1
        
        df = pd.DataFrame(candles)

        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.ewm(alpha=1/self.period, min_periods=self.period).mean()
        avg_loss = loss.ewm(alpha=1/self.period, min_periods=self.period).mean()

        rs = avg_gain / avg_loss
        rsi = (100 - (100 / (1 + rs))).iloc[-1]

        return round(float(rsi),3) if pd.notna(rsi) else -1

    def get_list_from_candles(self, candles):
        """
        Calculate Relative Strength Index (RSI) list from a list of OHLCV candles.

        Args:
            candles (list[dict]): List of dictionaries, each containing: open, high, low, close, volume
        Returns:
            list[float]: List of RSI values, with None for initial periods without enough data
        """
        if not candles or len(candles) < self.period:
            return []
        
        for candle in candles:
            if 'close' not in candle:
                return []

        temp_candles = candles.copy()
        rsi_list = []

        for i in range (len(temp_candles)):
            if not temp_candles or len(temp_candles) < self.period:
                rsi_list.append(None)
            else:
                rsi_list.append(self.calculate_rsi(temp_candles))
            temp_candles = temp_candles[:-1]

        return rsi_list[::-1]  # Reverzní seznam, aby odpovídal původnímu pořadí   

    def get_list_from_coin(self, coin: str, interval: str, candle_amount: int = 20):
        """
        Calculate Relative Strength Index (RSI) list from a list of OHLCV candles.

        Args:
            coin (str): Symbol, e.g., 'BTC/USDT'
            interval (str): Time interval, e.g., '1h', '1d'
            candle_amount (int): Number of candles to fetch, default is 20
        Returns:
            list[float]: List of RSI values, with None for initial periods without enough data
        """
        candles = get_binance_ohlcv(coin, interval, candle_amount)
        return self.get_list_from_candles(candles)  

    def get_signal_from_candles(self, candles):
        """
        Calculate RSI signals from a list of OHLCV candles with timestamps.

        Args:
            candles (list[dict]): List of dictionaries, each containing: open, high, low, close, volume
            
        Returns:
            str: 'BUY', 'SELL', or 'HOLD' based on the latest crossover signal. Return 'NOT ENOUGH DATA' if not enough data.
        """
        if not candles or len(candles) < self.period:
            return 'NOT ENOUGH DATA'

        RSI = self.calculate_rsi(candles)
        
        if RSI is None:
            return 'NOT ENOUGH DATA'

        # Poslední hodnoty RSI
        if pd.isna(RSI):
            return 'HOLD'
        elif RSI < self.oversold:
            return 'BUY'
        elif RSI > self.overbought:
            return 'SELL'
        else:
            return 'HOLD'
        
    def get_signal_from_coin(self, coin: str, interval: str):
        """
        Calculate RSI signal from a list of OHLCV candles with timestamps.

        Args:
            coin (str): Symbol, e.g., 'BTC/USDT'
            interval (str): Time interval, e.g., '1h', '1d'
            
        Returns:
            str: 'BUY', 'SELL', or 'HOLD' based on the latest rsi signal. Return 'NOT ENOUGH DATA' if not enough data.
        """

        candles = get_binance_ohlcv(coin, interval, candle_amount=self.period)
        return self.get_signal_from_candles(candles)

    def get_json(self) -> dict:
        return {
            "RSIStrategy": {
                "period": self.period,
                "oversold": self.oversold,
                "overbought": self.overbought
            }
        }

