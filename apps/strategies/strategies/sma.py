# apps/strategies/strategies/sma.py
import pandas as pd

from apps.strategies.strategies.base_strategy import BaseStrategy
from apps.strategies.strategies.base_indicator import BaseIndicator
from apps.market.services import get_binance_ohlcv

class SMAStrategy(BaseStrategy, BaseIndicator):
    def __init__(self, short_window: int = 10, long_window: int = 30):
        """
        Args:
            short_window (int): Period for short SMA (default 10)
            long_window (int): Period for long SMA (default 30)
        """
        self.short_window = short_window
        self.long_window = long_window

    def calculate_sma(self, candles, window: int):
        """
        Calculate Simple Moving Average (SMA) for the last candle from a list of OHLCV candles.

        Args:
            candles (list[dict]): List of dictionaries, each containing:
                - close
            window (int): Period for SMA
        Returns:
            float: Latest SMA value or -1 if not enough data
        """
        if not candles or len(candles) < window:
            return -1

        # Převod na DataFrame
        df = pd.DataFrame(candles, columns=['close'])
        df['SMA'] = df['close'].rolling(window).mean()
        value = df['SMA'].iloc[-1]

        return round(float(value),3) if pd.notna(value) else -1

    def get_list_from_candles(self, candles, window: int = None):
        """
        Calculate Simple Moving Average (SMA) list from a list of OHLCV candles.

        Args:
            candles (list[dict]): List of dictionaries, each containing:
                - open, high, low, close, volume
        
            window (int): Period for SMA. If None, uses short_window.
        Returns:
            list[float]: List of SMA values, with None for initial periods without enough data
        """
        if window is None:
            window = self.short_window

        if not candles or len(candles) < window:
            return []

        for candle in candles:
            if 'close' not in candle:
                return []
        
        temp_candles = candles.copy()
        sma_list = []

        for i in range (len(temp_candles)):
            if not temp_candles or len(temp_candles) < window:
                sma_list.append(None)
            else:
                sma_list.append(self.calculate_sma(temp_candles, window))
            temp_candles = temp_candles[:-1]

        return sma_list[::-1]  # Reverzní seznam, aby odpovídal původnímu pořadí   

    def get_list_from_coin(self, coin: str, interval: str, candle_amount: int = 20, window: int = None):
        """
        Calculate Simple Moving Average (SMA) list from a coin and interval.

        Args:   
            coin (str): Symbol, e.g., 'BTC/USDT'
            interval (str): Time interval, e.g., '1h', '1d'
            candle_amount (int): Number of candles to fetch, default is 20
            window (int): Period for SMA (default 10). If None, uses short_window.
        Returns:
            list[float]: List of SMA values, with None for initial periods without enough data
        """
        if window is None:
            window = self.short_window

        candles = get_binance_ohlcv(coin, interval, candle_amount)
        return self.get_list_from_candles(candles, window) 

    def get_signal_from_candles(self, candles):
        """
        Calculate SMA crossover signals from a list of OHLCV candles with timestamps.

        Args:
            candles (list[dict]): List of dictionaries, each containing:
                - open, high, low, close, volume
            
        Returns:
            str: 'BUY', 'SELL', or 'HOLD' based on the latest crossover signal. Return 'NOT ENOUGH DATA' if not enough data.
        """
        if not candles or len(candles) < self.long_window:
            return 'NOT ENOUGH DATA'

        SMA_short = self.calculate_sma(candles, self.short_window)
        SMA_long = self.calculate_sma(candles, self.long_window)
        
        if SMA_long is None or SMA_short is None:
            return 'NOT ENOUGH DATA'

        # Poslední hodnoty SMA
        if pd.isna(SMA_short) or pd.isna(SMA_long):
            return 'HOLD'

        if SMA_short > SMA_long:
            return 'BUY'
        elif SMA_short < SMA_long:
            return 'SELL'
        else:
            return 'HOLD'
        
    def get_signal_from_coin(self, coin: str, interval: str):
        """
        Calculate SMA crossover signals from a list of OHLCV candles with timestamps.

        Args:
            coin (str): Symbol, e.g., 'BTC/USDT'
            interval (str): Time interval, e.g., '1h', '1d'
            
        Returns:
            str: 'BUY', 'SELL', or 'HOLD' based on the latest crossover signal. Return 'NOT ENOUGH DATA' if not enough data.
        """

        candles = get_binance_ohlcv(coin, interval, candle_amount=self.long_window)
        return self.get_signal_from_candles(candles)

    def get_json(self) -> dict:
        return {
            "SMAStrategy": {
                "short_window": self.short_window,
                "long_window": self.long_window
            }
        }


