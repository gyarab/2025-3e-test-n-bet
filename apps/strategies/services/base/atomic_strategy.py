from abc import ABC, abstractmethod
import pandas as pd


class AtomicStrategy(ABC):
    """
    Abstract base class to define AtomicStrategies that can be used to craft a bigger one's, e.g. SMAStrategy, ARIMAStrategy, ..etc.
    Atomic Strategies are the building blocks for more complex strategies (called strategy conditions).
    Atomic Strategies contain either one indicator or one prediction model, but not more.
    Each Atomic Strategy should inherit from this class and implement its methods.
    """

    @abstractmethod
    def get_signal_from_coin(self, coin: str, interval: str) -> str:
        """
        Returns the latest signal based on the strategy for a given coin and interval.

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
    ) -> str:
        """
        Returns the latest signal based on the strategy for given candles.

        Args:
            candles (list[dict] | pd.DataFrame): OHLCV candles data.

        Returns:
            str: 'BUY', 'SELL', or 'HOLD'.
        """
        pass

    @abstractmethod
    def get_json(self) -> dict:
        """
        Returns the strategy parameters in JSON/dict format.

        Returns:
            dict: Dictionary representation of the strategy parameters.
        """
        pass
