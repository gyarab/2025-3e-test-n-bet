# apps/strategies/strategies/rsi.py
import pandas as pd

from apps.strategies.services.base.base_indicator import BaseIndicator
from apps.market.services import get_binance_ohlcv
from apps.strategies.services.indicators.rsi_indicator import RSIIndicator
from apps.strategies.services.base.indicator_strategy import IndicatorStrategy

class RSIStrategy(IndicatorStrategy):
    def __init__(self, rsi_indicator: RSIIndicator = None, oversold: int = 30, overbought: int = 70):
        """
        Args:
            rsi_indicator
            oversold (int): RSI value below which we buy (default 30)
            overbought (int): RSI value above which we sell (default 70)
        """
        if (oversold < 0 or overbought < 0) or (oversold >= overbought) or (oversold > 50) or (overbought > 100):
            raise ValueError("Invalid RSI thresholds: oversold must be >= 0, overbought must be > oversold, oversold <= 50, overbought <= 100.")

        rsi_indicator = rsi_indicator or RSIIndicator()
        self.rsi_indicator = rsi_indicator
        self.period = rsi_indicator.period
        self.oversold = oversold
        self.overbought = overbought

    @classmethod
    def from_parametrs(cls, period: int = 14, oversold: int = 30, overbought: int = 70):
        return cls(RSIIndicator(period=period), oversold=oversold, overbought=overbought)
    
    @classmethod
    def _from_json(cls, json_data: dict) -> 'RSIStrategy':
        """
        Create an RSIStrategy instance from JSON data.
        Get json data structure:
        {
            "period": 14,
            "oversold": 30,
            "overbought": 70
        }
        """
        period = json_data.get("period", 14)
        oversold = json_data.get("oversold", 30)
        overbought = json_data.get("overbought", 70)
        return cls.from_parametrs(period=period, oversold=oversold, overbought=overbought)

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

        RSI = self.rsi_indicator.calculate_rsi(candles)
        
        if RSI is None:
            return 'NOT ENOUGH DATA'

        # If some of the latest RSI values are NaN, return HOLD
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
            "name": "RSI Strategy",
            "parameters": {
                "period": self.period,
                "oversold": self.oversold,
                "overbought": self.overbought
            }
        }
    
    def indicator(self) -> BaseIndicator:
        return self.rsi_indicator

