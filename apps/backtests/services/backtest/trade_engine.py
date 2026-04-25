import random


class TradeEngine:
    """
    A class to execute a trade with entry and exit details.
    """

    def __init__(
        self,
        open_candle: dict[str, float],
        stop_loss_pct: float,
        take_profit_pct: float,
        quantity: float,
        trade_type: bool = True,
    ):
        """
        Obj: Trade object to represent a trade with entry and exit details.

        Args:
            candles (list[dict]): List of OHLCV candles, where the first candle is the trade-open candle.
            stop_loss_pct (float): Stop-loss in % > 0, e.g. 5 for 5%
            take_profit_pct (float): Take-profit in % > 0, e.g. 5 for 5%
            quantity (float): Quantity of the asset traded, in dollars
            trade_type (bool): True for buy trade, False for sell trade.
        """

        self.open_candle = open_candle
        self.entry_price = open_candle["open"] 
        self.open_time = open_candle["open_time"]

        self.quantity = quantity
        self.trade_type = trade_type  # True for buy, False for sell
        self.exit_price = 0  # Will be updated when trade is closed
        self.status = True  # True if trade is open, False if closed

        self.exit_time = None  # Will be updated when trade is closed

        self.stop_loss = (
            self.entry_price * (1 - stop_loss_pct / 100)
            if self.trade_type
            else self.entry_price * (1 + stop_loss_pct / 100)
        )
        self.take_profit = (
            self.entry_price * (1 + take_profit_pct / 100)
            if self.trade_type
            else self.entry_price * (1 - take_profit_pct / 100)
        )


    def get_result(self) -> float | None:
        """
        Calculate the result of the trade.

        Returns:
            float | None: The result of the trade (profit/loss amount) or None if trade is not closed.
        """
        if self.status == True:
            return None  # Trade not closed yet

        if self.trade_type:  # Buy trade
            return (self.exit_price / self.entry_price) * self.quantity - self.quantity
        else:  # Sell trade
            return (self.entry_price / self.exit_price) * self.quantity - self.quantity
        

    def execute(self, candles: list[dict]) -> float:
        """
        Execute the trade by iterating through all the candles and checking for stop-loss or take-profit hits.
        Candles should be in chronological order.

        Args:
            candles (list[dict]): List of OHLCV candles, where the first candle is the second one after the trade-open candle. Each candle should be a dictionary containing at least 'open', 'high', 'low', and 'open_time' keys.

        Returns:
            float: The result of the trade (profit/loss) or -1 if trade is not closed.
        """       

        for c in candles:
            if self._check_status(c):  # Trade is closed
                break

        return self.get_result()
    

    def update(self, candle: dict) -> None:
        """
        Update the trade status based on the next candle.

        Args:
            candle (dict): A dictionary containing OHLCV data for the current candle.
        """
        self._check_status(candle)


    def _check_status(self, candle: dict) -> bool:
        """
        Check if the trade should be closed based on the current candle. Sets exit_price and status if trade is closed.

        Args:
            candle (dict): A dictionary containing OHLCV data for the current candle.

        Returns:
            True if trade is closed, otherwise returns False. Sets exit_price if trade is closed, status to False.
        """

        EPS = 1e-9 # Small epsilon to handle floating-point precision issues

        low = candle["low"]
        high = candle["high"]

        # Define conditions based on trade direction
        if self.trade_type:  # Buy
            sl_hit = low <= self.stop_loss + EPS
            tp_hit = high >= self.take_profit - EPS
        else:  # Sell
            sl_hit = high >= self.stop_loss - EPS
            tp_hit = low <= self.take_profit + EPS

        # If both stop-loss and take-profit are hit in the same candle, we can randomly decide which one is hit first, or we can prioritize one over another. 
        # Here we will randomly decide, so the results will not be biased towards stop-loss hits in high-volatility candles. 
        if sl_hit and tp_hit:
            if random.random() < 0.5:
                self._close_trade(self.stop_loss, candle["open_time"])
            else:
                self._close_trade(self.take_profit, candle["open_time"])
            return True

        if sl_hit:
            self._close_trade(self.stop_loss, candle["open_time"])
            return True

        if tp_hit:
            self._close_trade(self.take_profit, candle["open_time"])
            return True

        return False
    
    def _close_trade(self, price: float, time) -> None:
        """
        Close the trade by setting the exit price, exit time, and status. 
        Args:
            price (float): The price at which the trade is closed (either stop-loss or take-profit price).
            time: The time at which the trade is closed (from the candle's open_time).
        """
        self.exit_price = price
        self.exit_time = time
        self.status = False

    def get_json(self) -> dict:
        return {
            "entry_price": self.entry_price,
            "exit_price": self.exit_price if not self.status else None,
            "entry_time": self.open_time,
            "exit_time": self.exit_time,
            "quantity": self.quantity,
            "trade_type": 1 if self.trade_type else 0, # 1 for buy, 0 for sell
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "status": 1 if self.status else 0, # 1 for open, 0 for closed
            "result": self.get_result() if not self.status else None, # Profit/loss amount
        }
