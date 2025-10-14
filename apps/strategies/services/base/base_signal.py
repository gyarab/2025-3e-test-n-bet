from abc import ABC, abstractmethod
from typing import Union, List
import pandas as pd

class BaseSignal(ABC):
    @abstractmethod
    def get_signal_from_candles(self, candles: Union[List[dict], pd.DataFrame]) -> str:
        """
        Returns 'BUY', 'SELL', or 'HOLD' based on given candles.
        """
        pass
