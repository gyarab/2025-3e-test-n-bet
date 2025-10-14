from abc import ABC, abstractmethod
import ccxt
import pandas as pd

from apps.strategies.services.base.base_indicator import BaseIndicator
from apps.strategies.services.base.base_signal import BaseSignal

class BaseStrategy(BaseSignal, ABC):
    """
    Abstract base class for all trading strategies.
    Each strategy should inherit from this class and implement its methods.
    """

    # Inicializace Binance
    exchange = ccxt.binance({
        'enableRateLimit': True
    })

    @abstractmethod
    def get_signal_from_coin(self, coin: str, interval: str) -> str:
        """
        Return the latest signal based on the strategy for a given coin and interval.

        Args:
            coin (str): Symbol, e.g., 'BTC/USDT'
            interval (str): Time interval, e.g., '1h', '1d'

        Returns:
            str: 'BUY', 'SELL', or 'HOLD'.
        """
        pass

    @abstractmethod
    def get_signal_from_candles(self, candles: list[dict[str, float]] | pd.DataFrame) -> str:
        """
        Return the latest signal based on the strategy for given candles.

        Args:
            candles (list[dict] | pd.DataFrame): OHLCV candles data.

        Returns:
            str: 'BUY', 'SELL', or 'HOLD'.
        """
        pass

    @abstractmethod
    def get_json(self) -> dict:
        """
        Return the strategy parameters in JSON/dict format.

        Returns:
            dict: Dictionary representation of the strategy parameters.
        """
        pass

    @abstractmethod
    def indicator(self) -> BaseIndicator:
        pass
