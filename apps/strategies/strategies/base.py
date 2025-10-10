from abc import ABC, abstractmethod
from typing import List, Dict, Union
import ccxt
import pandas as pd

class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    Each strategy should inherit from this class and implement its methods.
    """

    # Inicializace Binance
    exchange = ccxt.binance({
        'enableRateLimit': True
    })

    @abstractmethod
    def get_list(self, candles: Union[List[Dict], pd.DataFrame]) -> List[float]:
        """
        Return a list of indicator values (e.g., RSI list, SMA list) for given candles.

        Args:
            candles (list[dict] | pd.DataFrame): OHLCV candles data.

        Returns:
            list[float]: Indicator values.
        """
        pass

    @abstractmethod
    def get_signal(self, candles: Union[List[Dict], pd.DataFrame]) -> str:
        """
        Return the latest signal based on the strategy.

        Args:
            candles (list[dict] | pd.DataFrame): OHLCV candles data.

        Returns:
            str: 'BUY', 'SELL', or 'HOLD'.
        """
        pass

    @abstractmethod
    def get_json(self) -> Dict:
        """
        Return the strategy parameters in JSON/dict format.

        Returns:
            dict: Dictionary representation of the strategy parameters.
        """
        pass
