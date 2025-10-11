# apps/strategies/strategies/macd.py
import pandas as pd

from apps.strategies.services.base_strategy import BaseStrategy
from apps.strategies.services.base_indicator import BaseIndicator
from apps.market.services import get_binance_ohlcv

class MACDStrategy(BaseStrategy, BaseIndicator):
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        """
        Args:
            fast_period (int): Period for fast EMA (default 12)
            slow_period (int): Period for slow EMA (default 26)
            signal_period (int): Period for signal line EMA (default 9)
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def calculate_macd(self, candles: list[dict[str, float]]):
        """
        Calculate MACD line, signal line, and histogram for the last candle.

        Args:
            candles (list[dict]): List of dictionaries, each containing: close

        Returns:
            tuple: (macd_line, signal_line, histogram) or (-1, -1, -1) if not enough data
        """
        if not candles or len(candles) < self.slow_period:
            return -1, -1, -1  # not enough data

        df = pd.DataFrame(candles)
        close = df['close']

        ema_fast = close.ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = close.ewm(span=self.slow_period, adjust=False).mean()

        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False).mean()
        histogram = macd_line - signal_line

        return round(macd_line.iloc[-1], 3), round(signal_line.iloc[-1], 3), round(histogram.iloc[-1], 3)

    def get_list_from_candles(self, candles):
        """
        Calculates MACD line list from a list of OHLCV candles.

        Args:
            candles (list[dict]): List of dictionaries, each containing:
                - open, high, low, close, volume
        Returns:
            list[float]: List of MACD values, with None for initial periods without enough data
        """
        if not candles or len(candles) < self.slow_period:
            return []

        for candle in candles:
            if 'close' not in candle:
                return []
        
        df = pd.DataFrame(candles)
        ema_fast = df['close'].ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = df['close'].ewm(span=self.slow_period, adjust=False).mean()
        macd_line = ema_fast - ema_slow 

        return macd_line.round(3).tolist()

    def get_list_from_coin(self, coin: str, interval: str, candle_amount: int = 20):
        """
        Calculate MACD line list from a coin and interval.

        Args:   
            coin (str): Symbol, e.g., 'BTC/USDT'
            interval (str): Time interval, e.g., '1h', '1d'
            candle_amount (int): Number of candles to fetch, default is 20
        Returns:
            list[float]: List of SMA values, with None for initial periods without enough data
        """

        candles = get_binance_ohlcv(coin, interval, candle_amount)
        return self.get_list_from_candles(candles) 

    def get_signal_from_candles(self, candles):
        """
        Calculate MACD signals from a list of OHLCV candles with timestamps.

        Args:
            candles (list[dict]): List of dictionaries, each containing:
                - open, high, low, close, volume
            
        Returns:
            str: 'BUY', 'SELL', or 'HOLD' based on the latest crossover signal. Return 'NOT ENOUGH DATA' if not enough data.
        """
        if len(candles) < self.slow_period + 1:
            return "NOT ENOUGH DATA"

        # MACD for last two candles to detect crossover
        macd_line_1, signal_line_1, _ = self.calculate_macd(candles[:-1])
        macd_line_2, signal_line_2, _ = self.calculate_macd(candles)

        if macd_line_1 is None or macd_line_2 is None:
            return "NOT ENOUGH DATA"

        if macd_line_1 <= signal_line_1 and macd_line_2 > signal_line_2:
            return "BUY"
        elif macd_line_1 >= signal_line_1 and macd_line_2 < signal_line_2:
            return "SELL"
        else:
            return "HOLD"
        
    def get_signal_from_coin(self, coin: str, interval: str):
        """
        Calculate MACD crossover signals from a list of OHLCV candles with timestamps.

        Args:
            coin (str): Symbol, e.g., 'BTC/USDT'
            interval (str): Time interval, e.g., '1h', '1d'
            
        Returns:
            str: 'BUY', 'SELL', or 'HOLD' based on the latest crossover signal. Return 'NOT ENOUGH DATA' if not enough data.
        """

        candles = get_binance_ohlcv(coin, interval, candle_amount=self.slow_period + 1)
        return self.get_signal_from_candles(candles)

    def get_json(self) -> dict:
        return {
            "MACDStrategy": {
                "fast_period": self.fast_period,
                "slow_period": self.slow_period,
                "signal_period": self.signal_period
            }
        }


