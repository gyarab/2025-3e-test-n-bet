from abc import ABC, abstractmethod
from typing import Union
import ccxt
import pandas as pd

class BaseIndicator(ABC):
    """
    Abstract base class for all indicators
    Each indicator should inherit from this class and implement its methods.
    """

    @abstractmethod
    def get_list_from_candles(self, candles: list[dict[str, float]] | pd.DataFrame) -> list[float]:
        """
        Return a list of indicator values (e.g., RSI list, SMA list) for given candles.

        Args:
            candles (list[dict] | pd.DataFrame): OHLCV candles data.

        Returns:
            list[float]: Indicator values.
        """
        pass

    @abstractmethod
    def get_list_from_coin(self, coin: str, interval: str) -> list[float]:
        """
        Return a list of indicator values (e.g., RSI list, SMA list) for given coin.

        Args:
            coin (str): Symbol, e.g., 'BTC/USDT'
            interval (str): Time interval, e.g., '1h', '1d'

        Returns:
            list[float]: Indicator values.
        """
        pass

    @abstractmethod
    def calculate(self, candles: list[dict[str, float]], *args) -> Union[float, tuple[float, ...]]:
        """
        Returns a result after indicator's calculations on the set of candles based on indicator's parametrs
        """
        pass
