from abc import ABC, abstractmethod
import ccxt
import pandas as pd

class BasePredictionModel(ABC):
    """
    Abstract base class for all prediction models. Not implemented yet.
    Each prediction model should inherit from this class and implement its methods.
    """

    @abstractmethod
    def get_prediction_list(self, coin: str, interval: str) -> str:
        pass

    @abstractmethod
    def get_json(self) -> dict:
        pass