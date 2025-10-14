# apps/strategies/strategies/rsi.py
import pandas as pd

from apps.strategies.services.base.base_strategy import BaseStrategy
from apps.strategies.services.base.base_indicator import BaseIndicator
from apps.market.services import get_binance_ohlcv
from apps.strategies.services.indicators.rsi_indicator import RSIIndicator
from apps.strategies.services.base.atomic_strategy import AtomicStrategy
from apps.strategies.services.base.indicator_strategy import IndicatorStrategy

class RSIStrategy(IndicatorStrategy):
    def __init__(self, rsi_indicator: RSIIndicator = None, oversold: int = 30, overbought: int = 70):
        """
        Args:
            rsi_indicator
            oversold (int): RSI value below which we buy (default 30)
            overbought (int): RSI value above which we sell (default 70)
        """
        rsi_indicator = rsi_indicator or RSIIndicator()
        self.rsi_indicator = rsi_indicator
        self.period = rsi_indicator.period
        self.oversold = oversold
        self.overbought = overbought

    @classmethod
    def from_parametrs(cls, period: int = 14, oversold: int = 30, overbought: int = 70):
        return cls(RSIIndicator(period=period), oversold=oversold, overbought=overbought)

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
            "name": "RSI Strategy",
            "parameters": {
                "period": self.period,
                "oversold": self.oversold,
                "overbought": self.overbought
            }
        }
    
    def indicator(self) -> BaseIndicator:
        return self.rsi_indicator

