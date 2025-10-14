import pandas as pd

from apps.market.services import get_binance_ohlcv
from apps.strategies.services.base.base_indicator import BaseIndicator


class MACDIndicator(BaseIndicator):
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
    
    def calculate_macd(self, candles: list[dict[str, float]]) -> tuple[float, float, float]:
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

    def calculate(self, candles) -> tuple[float, float, float]:
        return self.calculate_macd(candles)