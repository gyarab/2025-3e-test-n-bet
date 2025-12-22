import pandas as pd

from apps.strategies.services.base.base_strategy import BaseStrategy
from apps.strategies.services.base.base_indicator import BaseIndicator
from apps.market.services import get_binance_ohlcv
from apps.strategies.services.indicators.macd_indicator import MACDIndicator
from apps.strategies.services.base.atomic_strategy import AtomicStrategy
from apps.strategies.services.base.indicator_strategy import IndicatorStrategy

class MACDStrategy(IndicatorStrategy):
    def __init__(self, macd_indicator: MACDIndicator = None, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        """
        Args:
            macd_indicator
            fast_period (int): Period for fast EMA (default 12)
            slow_period (int): Period for slow EMA (default 26)
            signal_period (int): Period for signal line EMA (default 9)
        """
        if (fast_period < 1 or slow_period < 1 or signal_period < 1) or (fast_period >= slow_period) or (fast_period > 50) or (slow_period > 100) or (signal_period > 50):
            raise ValueError("Invalid MACD parameters: fast_period must be > 0, slow_period must be > fast_period, signal_period must be > 0, fast_period <= 50, slow_period <= 100, signal_period <= 50.")

        self.macd_indicator = macd_indicator or MACDIndicator(fast_period=fast_period, slow_period=slow_period, signal_period=signal_period)
        self.fast_period = self.macd_indicator.fast_period 
        self.slow_period = self.macd_indicator.slow_period
        self.signal_period = self.macd_indicator.signal_period 

    @classmethod
    def from_parametrs(cls, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        return cls(MACDIndicator(fast_period=fast_period, slow_period=slow_period, signal_period=signal_period))
        

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
        macd_line_1, signal_line_1, _ = self.macd_indicator.calculate_macd(candles[:-1])
        macd_line_2, signal_line_2, _ = self.macd_indicator.calculate_macd(candles)

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
            "name": "MACD Strategy",
            "parameters": {
                "fast_period": self.fast_period,
                "slow_period": self.slow_period,
                "signal_period": self.signal_period
            }
        }
    
    def indicator(self) -> BaseIndicator:
        return self.macd_indicator


