from abc import ABC, abstractmethod
import ccxt
import pandas as pd

class BaseModel(ABC):

    @abstractmethod
    def get_prediction_list(self, coin: str, interval: str) -> str:
        pass

    @abstractmethod
    def get_json(self) -> dict:
        pass