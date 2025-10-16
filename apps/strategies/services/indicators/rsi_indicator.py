import pandas as pd

from apps.market.services import get_binance_ohlcv
from apps.strategies.services.base.base_indicator import BaseIndicator


class RSIIndicator(BaseIndicator):
    def __init__(self, period: int = 14):
        """
        Args:
            period ()
        """
        self.period = period

    def calculate_rsi(self, candles) -> float:
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
    
    def calculate(self, candles, *args) -> float:
        return self.calculate_rsi(candles)
    
    def get_list_from_candles(self, candles) -> list[float]:
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