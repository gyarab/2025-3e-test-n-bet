class TradeRiskModel:
    """
    Manages trade risk parameters like stop-loss and take-profit.
    Supports fixed percentage and ATR-based relative calculations.
    """

    def __init__(self, 
                 stop_loss_pct: float = 5, 
                 stop_loss_type: str = 'fixed', 
                 take_profit_pct: float = 10, 
                 take_profit_type: str = 'fixed', 
                 position_size_pct: float = 5,
                 position_size_type: str = 'fixed', 
                 candles: list[dict] = None):
        """
        Initialize the TradeRiskModel with default or specified parameters.

        Args:
            stop_loss_pct (float): Stop-loss percentage for 'fixed' type. Ignored if 'relative'.
            stop_loss_type (str): 'fixed' or 'relative'. Fixed uses a constant percentage, relative uses ATR-based volatility.
            take_profit_pct (float): Take-profit percentage for 'fixed' type. Ignored if 'relative'.
            take_profit_type (str): 'fixed' or 'relative'. Fixed uses a constant percentage, relative is based on stop-loss.
            position_size_pct (float): Percentage for fixed position size. Ignored if type is 'relative'.
            position_size_type (str): 'fixed' or 'relative'. Fixed uses a constant percentage of account balance, relative adjusts based on loss percentage.
            candles (list[dict]): List of OHLCV candles, where last candle is the entry candle. Required if stop_loss_type is 'relative'.
        """
        self.stop_loss_pct = None
        self.stop_loss_type = stop_loss_type
        self.take_profit_pct = None
        self.take_profit_type = take_profit_type
        self.position_size_pct = None
        self.position_size_type = position_size_type      
        
        self.set_stop_loss(stop_loss_type=stop_loss_type, stop_loss_pct=stop_loss_pct, candles=candles)
        self.set_take_profit(take_profit_type=take_profit_type, take_profit_pct=take_profit_pct)
        self.set_position_size(position_size_type=position_size_type, position_size_pct=position_size_pct)

    def set_position_size(self, position_size_type: str = 'fixed', position_size_pct: float = 5, loss_percetage: float = 2) -> None:
        """
        Set the position size percentage and type.
        Args:
            position_size_type (str): 'fixed' or 'relative'.
                - 'fixed' uses a constant percentage of account balance.
                - 'relative' adjusts position size based on the loss percentage (calculated as loss_percentage / stop_loss_percentage).
            position_size_pct (float): Percentage for fixed position size. Ignored if type is 'relative'.
            loss_percetage (float): Percentage of account balance willing to risk per trade. Used if type is 'relative'.
        """
        if position_size_type not in ['fixed', 'relative', 'sl-based']:
            raise ValueError("Invalid position_size_type. Use 'fixed' or 'relative'.")
        
        if position_size_type == 'fixed':
            self.position_size_pct = position_size_pct
            self.position_size_type = position_size_type
        elif position_size_type == 'relative':
            if not hasattr(self, 'stop_loss_pct'):
                raise ValueError("Set stop_loss before setting position_size with relative type.")
            self.position_size_pct = loss_percetage / self.stop_loss_pct * 100
            self.position_size_type = position_size_type
    
    def set_stop_loss(self, stop_loss_type: str = 'fixed', stop_loss_pct: float = 5, candles: list[dict] = None) -> float:
        """
        Set the stop-loss percentage and type.
        Args:
            stop_loss_type (str): 'fixed' or 'relative'. Fixed uses a constant percentage, relative uses ATR-based volatility.
            stop_loss_pct (float): Percentage for fixed stop-loss. Ignored if type is 'relative'.
            candles (list[dict]): List of OHLCV candles, , where last candle is the entry candle. Required if stop_loss_type is 'relative'.
        Returns:
            float: The stop-loss percentage.
        """
        if stop_loss_type not in ['fixed', 'relative']:
            raise ValueError("Invalid stop_loss_type. Use 'fixed' or 'relative'.")

        if self.stop_loss_type == 'fixed':
            self.stop_loss_pct = stop_loss_pct
            self.stop_loss_type = stop_loss_type
        elif self.stop_loss_type == 'relative':
            if candles is None:
                raise ValueError("Candles data required for relative stop-loss calculation.")
            self.stop_loss_pct = self._calculate_relative_stop_loss_percentage(candles)
            self.stop_loss_type = stop_loss_type
        else:
            raise ValueError("Invalid stop_loss_type. Use 'fixed' or 'relative'.")
        
        return self.stop_loss_pct
    
    def set_take_profit(self, take_profit_type: str = 'fixed', take_profit_pct: float = 5, multiplier: float = 2.0) -> float:
        """
        Set the stop-loss percentage and type.
        Args:
            take_profit_type (str): 'fixed' or 'relative'
            take_profit_pct (float): Percentage for fixed take-profit. Ignored if type is 'relative'.
            multiplier (float): Multiplier for relative take-profit, which is calculated as stop_loss * multiplier. Ignored if type is 'fixed'.
        Returns:
            float: The stop-loss percentage.
        """
        if take_profit_type not in ['fixed', 'relative']:
            raise ValueError("Invalid take_profit_type. Use 'fixed' or 'relative'.")

        if self.stop_loss_type == 'fixed':
            self.take_profit_pct = take_profit_pct
            self.take_profit_type = take_profit_type
        elif self.stop_loss_type == 'relative':
            if not hasattr(self, 'stop_loss_pct'):
                raise ValueError("Set stop_loss before setting take_profit with relative type.")
            self.take_profit_pct = self.stop_loss_pct * multiplier
            self.take_profit_type = take_profit_type
        else:
            raise ValueError("Invalid stop_loss_type. Use 'fixed' or 'relative'.")
        
        return self.stop_loss_pct
    
    def get_stop_loss(self) -> float:
        return self.stop_loss_pct
    
    def get_take_profit(self) -> float:
        return self.take_profit_pct
    
    def get_json(self) -> dict: #Maybe change depending on the frontend
        """
        Return a JSON-serializable dictionary representing the trade risk configuration.
        """
        return {
            "stop_loss": {
                "type": self.stop_loss_type,
                "percentage": self.stop_loss_pct
            },
            "take_profit": {
                "type": self.take_profit_type,
                "percentage": self.take_profit_pct
            },
            "position_size": {
                "type": self.position_size_type,
                "percentage": self.position_size_pct
            }
    }


    def calculate_stop_loss_price(entry_price: float, current_price: float, percentage: float) -> float:
        """
        Calculate the stop-loss price based on entry price and a percentage.

        Args:
            entry_price (float): The price at which the position was entered.
            current_price (float): The current market price.
            percentage (float): The stop-loss percentage (e.g., 0.05 for 5%).

        Returns:
            float: The calculated stop-loss price.
        """
        if entry_price <= 0 or percentage <= 0:
            raise ValueError("Entry price and percentage must be positive values.")

        stop_loss_price = entry_price * (1 - percentage)
        return round(stop_loss_price, 2)

    def calculate_take_profit_price(entry_price: float, current_price: float, percentage: float) -> float:
        """
        Calculate the take-profit price based on entry price and a percentage.

        Args:
            entry_price (float): The price at which the position was entered.
            current_price (float): The current market price.
            percentage (float): The take-profit percentage (e.g., 0.10 for 10%).

        Returns:
            float: The calculated take-profit price.
        """
        if entry_price <= 0 or percentage <= 0:
            raise ValueError("Entry price and percentage must be positive values.")

        take_profit_price = entry_price * (1 + percentage)
        return round(take_profit_price, 2)

    def _calculate_relative_stop_loss_percentage(candles: list[dict], period: int = 14, atr_multiplier: float = 1.5) -> float:
        """
        Calculate relative stop loss based on ATR volatility.
        
        Args:
            entry_price (float): The trade entry price.
            candles (list[dict]): Candle data containing in ohlcv format, where last candle's 'close' attribute is the entry price.
            period (int): ATR lookback period (default=14).
            atr_multiplier (float): How many ATRs away the stop loss is.
        
        Returns:
            float: Stop loss percentage (e.g. 2.5 for 2.5%).
        """
        
        if len(candles) < period + 1:
            raise ValueError("Not enough candle data to compute ATR")
        
        recent_candles = candles[-(period + 1):]
        true_ranges = []
        entry_price = candles[-1]["close"]
        
        for i in range(1, len(recent_candles)):
            high = recent_candles[i]["high"]
            low = recent_candles[i]["low"]
            prev_close = recent_candles[i - 1]["close"]

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)

        # Average True Range
        atr = sum(true_ranges[-period:]) / period

        # Relative stop loss percentage based on entry price
        stop_loss_pct = (atr_multiplier * atr / entry_price) * 100

        return stop_loss_pct
    
    @classmethod
    def _from_json(cls, json_data: dict) -> 'TradeRiskModel':
        """
        Create a TradeRiskModel instance from a JSON dictionary.

        Args:
            json_data (dict): JSON dictionary with keys 'stop_loss', 'take_profit', and 'position_size'.
        
        Returns:
            TradeRiskModel: An instance of TradeRiskModel initialized with the provided parameters.
        """
        pass
    


