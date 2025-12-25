# apps/strategies/strategies/sma.py
import pandas as pd

from apps.strategies.services.base.base_strategy import BaseStrategy
from apps.strategies.services.base.base_indicator import BaseIndicator
from apps.market.services import get_binance_ohlcv
from apps.strategies.services.indicators.sma_indicator import SMAIndicator
from apps.strategies.services.base.atomic_strategy import AtomicStrategy
from apps.strategies.services.base.indicator_strategy import IndicatorStrategy

class SMAStrategy(IndicatorStrategy):
    def __init__(self, sma_indicator: SMAIndicator = None, short_window: int = 10, long_window: int = 30):
        """
        Args:
            short_window (int): Period for short SMA (default 10)
            long_window (int): Period for long SMA (default 30)
        """
        if (short_window < 1 or long_window < 2) or (short_window >= long_window) or (short_window > 50) or (long_window > 300):
            raise ValueError("Invalid window sizes: short_window must be > 1, long_window must be > short_window, short_window <= 50, long_window <= 300.")

        sma_indicator = sma_indicator or SMAIndicator()
        self.sma_indicator = sma_indicator
        self.short_window = short_window
        self.long_window = long_window

    @classmethod
    def from_parametrs(cls, short_window: int = 10, long_window: int = 30):
        return cls(SMAIndicator(window=short_window), short_window=short_window, long_window=long_window)
    
    @classmethod
    def _from_json(cls, json_data: dict) -> 'SMAStrategy':
        """
        Create an SMAStrategy instance from JSON data.
        Get json data structure:
        {
            "short_window": 10,
            "long_window": 30
        }
        """
        short_window = json_data.get("short_window", 10)
        long_window = json_data.get("long_window", 30)
        return cls.from_parametrs(short_window=short_window, long_window=long_window)

    def get_signal_from_candles(self, candles) -> str:
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

        SMA_short = self.indicator().calculate(candles, self.short_window)
        SMA_long = self.indicator().calculate(candles, self.long_window)

        SMA_long_previous = self.indicator().calculate(candles[:-1], self.long_window)
        SMA_short_previous = self.indicator().calculate(candles[:-1], self.short_window)
        
        if SMA_long is None or SMA_short is None or SMA_long_previous is None or SMA_short_previous is None:
            return 'NOT ENOUGH DATA'

        # Check for NaN values
        if pd.isna(SMA_short) or pd.isna(SMA_long):
            return 'HOLD'

        if SMA_short > SMA_long and SMA_short_previous <= SMA_long_previous:
            return 'BUY'
        elif SMA_short < SMA_long and SMA_short_previous >= SMA_long_previous:
            return 'SELL'
        else:
            return 'HOLD'
        
    def get_signal_from_coin(self, coin: str, interval: str) -> str:
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
            "name": "SMA Strategy",
            "parameters": {
                "short_window": self.short_window,
                "long_window": self.long_window
            }
        }
    
    def indicator(self) -> BaseIndicator:
        return self.sma_indicator


