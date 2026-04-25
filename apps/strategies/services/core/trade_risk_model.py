class TradeRiskModel:
    """
    Manages trade risk parameters like stop-loss and take-profit.
    Supports fixed percentage and ATR-based relative calculations.
    """

    def __init__(
        self,
        stop_loss_pct: float = 1.5,
        stop_loss_type: str = "fixed",
        take_profit_pct: float = 5.0,
        take_profit_type: str = "fixed",
        position_size_pct: float = 3,
        position_size_type: str = "fixed"
    ):
        """
        Initialize the TradeRiskModel with default or specified parameters.

        Args:
            stop_loss_pct (float): Stop-loss percentage for 'fixed' type. Ignored if 'relative'.
            stop_loss_type (str): 'fixed' or 'relative'. Fixed uses a constant percentage, relative uses ATR-based volatility.
            take_profit_pct (float): Take-profit percentage for 'fixed' type. Ignored if 'relative'.
            take_profit_type (str): 'fixed' or 'relative'. Fixed uses a constant percentage, relative is based on stop-loss.
            position_size_pct (float): Used as a fixed percentage of the balance to calculate the quantity if 'fixed'. Used as max loss percentage to calculate the quantity if 'relative'.
            position_size_type (str): 'fixed' or 'relative'. Fixed uses a constant percentage of account balance, relative adjusts based on loss percentage.
        """

        if stop_loss_type not in ["fixed", "relative"]:
            raise ValueError("Invalid stop_loss_type. Use 'fixed' or 'relative'.")
        
        self.stop_loss_type = stop_loss_type
        self.stop_loss_pct = float(stop_loss_pct)

        if take_profit_type not in ["fixed", "relative"]:
            raise ValueError("Invalid take_profit_type. Use 'fixed' or 'relative'.")
        
        self.take_profit_type = take_profit_type
        self.take_profit_pct = float(take_profit_pct) # When using relative take-profit, this is treated as a multiplier of the stop-loss percentage (e.g., 2 means take-profit is set at 2 times the stop-loss distance).

        if position_size_type not in ["fixed", "relative"]:
            raise ValueError("Invalid position_size_type. Use 'fixed' or 'relative'")
        
        self.position_size_type = position_size_type
        self.position_size_pct = float(position_size_pct) # When using relative position sizing, this is treated as the risk per trade percentage of the account balance.


    def set_position_size(self) -> float:
        """
        Set the position size percentage and type. 
        If using relative position sizing, this calculates the position size percentage based on the risk per trade and stop-loss percentage.
        
        Returns:
            float: The position size percentage.
        """

        risk_per_trade = self.position_size_pct # When using relative position sizing, the position_size_pct is treated as the risk per trade percentage of the account balance.

        if self.position_size_type == "relative":
            if not hasattr(self, "stop_loss_pct"):
                raise ValueError("Set stop_loss before setting position_size.")

            return risk_per_trade / self.stop_loss_pct

        return self.position_size_pct


    def set_stop_loss(self, candles: list[dict] = None) -> float:
        """
        Set the stop-loss percentage and type. 
        If using relative stop-loss, this calculates the stop-loss percentage based on ATR volatility.

        Args:
            candles (list[dict]): List of OHLCV candles, , where last candle is the entry candle. Required if stop_loss_type is 'relative'.

        Returns:
            float: The stop-loss percentage.
        """
        if self.stop_loss_type not in ["fixed", "relative"]:
            raise ValueError("Invalid stop_loss_type. Use 'fixed' or 'relative'.")

        if self.stop_loss_type == "relative":
            if candles is None:
                raise ValueError(
                    "Candles data required for relative stop-loss calculation."
                )
            self.stop_loss_pct = self._calculate_relative_stop_loss_percentage(candles)
            
        return self.stop_loss_pct
    

    def set_take_profit(self) -> float:
        """
        Set the stop-loss percentage and type. 
        If using relative take-profit, this calculates the take-profit percentage based on the stop-loss percentage and a multiplier.

        Returns:
            float: The stop-loss percentage.
        """

        multiplier = self.take_profit_pct # When using relative take-profit, the take_profit_pct is treated as a multiplier of the stop-loss percentage (e.g., 2 means take-profit is set at 2 times the stop-loss distance).

        if self.stop_loss_type == "relative":
            if not hasattr(self, "stop_loss_pct"):
                raise ValueError(
                    "Set stop_loss before setting take_profit with relative type."
                )
            return self.stop_loss_pct * multiplier

        return self.take_profit_pct
    
    
    def reload_values(self, candles: list[dict]) -> None:
        """
        Recalculate stop-loss and take-profit percentages based on the latest candle data.

        Args:
            candles (list[dict]): List of OHLCV candles, where last candle is the entry candle.
        """
        self.set_stop_loss(candles)
        self.set_take_profit()
        self.set_position_size()


    def get_stop_loss(self, candles) -> float:
        self.reload_values(candles)
        return self.stop_loss_pct

    def get_take_profit(self, candles) -> float:
        self.reload_values(candles)
        return self.take_profit_pct
    
    def get_position_quantity(self, account_balance: float, candles: list[dict]) -> float:
        """
        Calculate position quantity based on account balance and position size settings.

        Args:
            account_balance (float): Current account balance.

        Returns:
            float: Calculated position quantity in dollars.
        """
        self.reload_values(candles)

        quantity = (self.position_size_pct / 100) * account_balance

        return round(quantity, 2)


    def _calculate_relative_stop_loss_percentage(self, 
        candles: list[dict], period: int = 14, atr_multiplier: float = 5
    ) -> float:
        """
        Calculate relative stop loss based on ATR volatility.

        Args:
            entry_price (float): The trade entry price.
            candles (list[dict]): Candle data containing in ohlcv format, where last candle's 'close' attribute is the entry price.
            period (int): ATR lookback period (default=14).
            atr_multiplier (float): How many ATRs away the stop loss is set (default=5).

        Returns:
            float: Stop loss percentage (e.g. 2.5 for 2.5%).
        """

        if len(candles) < period + 1:
            return self.stop_loss_pct  # Not enough data to calculate ATR, return default stop loss percentage

        recent_candles = candles[-(period + 1) :]
        true_ranges = []
        entry_price = candles[-1]["close"]

        for i in range(1, len(recent_candles)):
            high = recent_candles[i]["high"]
            low = recent_candles[i]["low"]
            prev_close = recent_candles[i - 1]["close"]

            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            true_ranges.append(tr)

        # Average True Range
        atr = sum(true_ranges[-period:]) / period

        # Relative stop loss percentage based on entry price
        stop_loss_pct = (atr_multiplier * atr / entry_price) * 100

        return stop_loss_pct
    

    def get_json(self) -> dict:
        """
        Return a JSON-serializable dictionary representing the trade risk configuration.
        """
        return {
            "stop_loss": {
                "type": self.stop_loss_type,
                "percentage": self.stop_loss_pct,
            },
            "take_profit": {
                "type": self.take_profit_type,
                "percentage": self.take_profit_pct,
            },
            "position_size": {
                "type": self.position_size_type,
                "percentage": self.position_size_pct,
            },
        }
    

    @staticmethod
    def calculate_stop_loss_price(
        entry_price: float, percentage: float
    ) -> float:
        """
        Calculate the stop-loss price based on entry price and a percentage.

        Args:
            entry_price (float): The price at which the position was entered.
            percentage (float): The stop-loss percentage (e.g., 0.05 for 5%).

        Returns:
            float: The calculated stop-loss price.
        """
        if entry_price <= 0 or percentage <= 0:
            raise ValueError("Entry price and percentage must be positive values.")

        stop_loss_price = entry_price * (1 - percentage)
        return round(stop_loss_price, 2)


    @staticmethod
    def calculate_take_profit_price(
        entry_price: float, percentage: float
    ) -> float:
        """
        Calculate the take-profit price based on entry price and a percentage.

        Args:
            entry_price (float): The price at which the position was entered.
            percentage (float): The take-profit percentage (e.g., 0.10 for 10%).

        Returns:
            float: The calculated take-profit price.
        """
        if entry_price <= 0 or percentage <= 0:
            raise ValueError("Entry price and percentage must be positive values.")

        take_profit_price = entry_price * (1 + percentage)
        return round(take_profit_price, 2)


    @classmethod
    def _from_json(cls, json_data: dict) -> "TradeRiskModel":
        """
        Create a TradeRiskModel instance from a JSON dictionary.

        Expected JSON structure:
        {
            "stop_loss": {"type": "fixed", "percentage": 1.5},
            "take_profit": {"type": "fixed", "percentage": 3.0},
            "position_size": {"type": "relative", "percentage": 2.0}
        }

        Args:
            json_data (dict): JSON dictionary with keys 'stop_loss', 'take_profit', and 'position_size'.

        Returns:
            TradeRiskModel: An instance of TradeRiskModel initialized with the provided parameters.
        """
        stop_loss_data = json_data.get("stop_loss", {})
        take_profit_data = json_data.get("take_profit", {})
        position_size_data = json_data.get("position_size", {})

        return cls(
            stop_loss_type=stop_loss_data.get("type", "fixed"),
            stop_loss_pct=stop_loss_data.get("percentage", 1.5),
            take_profit_type=take_profit_data.get("type", "fixed"),
            take_profit_pct=take_profit_data.get("percentage", 3.0),
            position_size_type=position_size_data.get("type", "fixed"),
            position_size_pct=position_size_data.get("percentage", 2.0),
        )
