import pandas as pd

from apps.market.services import get_binance_ohlcv
from apps.strategies.services.base.base_indicator import BaseIndicator


class SMAIndicator(BaseIndicator):
    def __init__(self, window: int = 10):
        self.window = window

    def calculate_sma(self, candles, window: int) -> float:
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
    
    def calculate(self, candles, window=10) -> float:
        return self.calculate_sma(candles, window=window)

    def get_list_from_candles(self, candles, window: int = None) -> list[float]:
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
            window = self.window

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

    def get_list_from_coin(self, coin: str, interval: str, candle_amount: int = 20, window: int = None) -> list[float]:
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
            window = self.window

        candles = get_binance_ohlcv(coin, interval, candle_amount)
        return self.get_list_from_candles(candles, window) 