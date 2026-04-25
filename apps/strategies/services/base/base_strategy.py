from abc import ABC, abstractmethod
import ccxt
import pandas as pd

from apps.strategies.services.base.base_indicator import BaseIndicator
from apps.strategies.services.core.trade_risk_model import TradeRiskModel


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    Each strategy should inherit from this class and implement its methods.
    """

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
    def get_signal_from_candles(
        self, candles: list[dict[str, float]] | pd.DataFrame
    ) -> tuple[str, TradeRiskModel]:
        """
        Return the latest signal based on the strategy for given candles.

        Args:
            candles (list[dict] | pd.DataFrame): OHLCV candles data.

        Returns:
            tuple[str, TradeRiskModel]: A tuple containing the signal ('BUY', 'SELL', or 'HOLD') and the associated TradeRiskModel.
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
