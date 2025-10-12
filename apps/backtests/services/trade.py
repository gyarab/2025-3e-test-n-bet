class Trade():
    """
    A class to execute a trade with entry and exit details.
    """

    #TODO fix bug that if price hits take profit and stop loss in the same candle, it always counts as stop loss. 
    # If we keep it this way, then all the high-volatility candles will be counted as stop loss hits, which may be not so crucial, 
    # as high-volatility means manipulations and counting profitable trades based on manipulations is not correct.

    def __init__(self, candles: list[dict], stop_loss_pct: float, take_profit_pct: float, quantity: float, trade_type: bool = True):
        """
        Obj: Trade object to represent a trade with entry and exit details.
        
        Args:
            candles (list[dict]): List of OHLCV candles, where the first candle is the trade-open candle.
            stop_loss_pct (float): Stop-loss in % > 0, e.g. 5 for 5%
            take_profit_pct (float): Take-profit in % > 0, e.g. 5 for 5%
            quantity (float): Quantity of the asset traded, in dollars
            trade_type (bool): True for buy trade, False for sell trade.
        """
        self.candles = candles
        self.entry_price = candles[0]['open']  # Entry price is the open price of the first candle
        self.quantity = quantity

        self.trade_type = trade_type  # True for buy, False for sell
        self.exit_price = 0  # Will be updated when trade is closed
        self.status = True  # True if trade is open, False if closed

        self.stop_loss = self.entry_price * (1 - stop_loss_pct/100) if self.trade_type else self.entry_price * (1 + stop_loss_pct/100)
        self.take_profit = self.entry_price * (1 + take_profit_pct/100) if self.trade_type else self.entry_price * (1 - take_profit_pct/100)

    def get_result(self) -> float:
        """
        Calculate the result of the trade.  
        Returns:
            float: The result of the trade (profit/loss) or -1 if trade is not closed.
        """
        if self.status == True:
            return -1  # Trade not closed yet

        if self.trade_type:  # Buy trade
            return (self.exit_price/self.entry_price) * self.quantity - self.quantity
        else:  # Sell trade
            return (self.entry_price/self.exit_price) * self.quantity - self.quantity
    
    def execute(self) -> float:
        """
        Execute the trade by iterating through the candles and checking for stop-loss or take-profit hits.
        Returns:
            float: The result of the trade (profit/loss) or -1 if trade is not closed.
        """
        for c in self.candles[1:]:  # Start checking from the second candle
            result = self._check_status(c)
            if result:  # Trade is closed
                break

        return self.get_result()
        
    def _check_status(self, candle: dict) -> bool:
        """
        Check if the trade should be closed based on the current candle. Sets exit_price and status if trade is closed.

        Args:
            candle (dict): A dictionary containing OHLCV data for the current candle.

        Returns: 
            True if trade is closed, otherwise returns False. Sets exit_price if trade is closed, status to False. 
        """
        if self.trade_type:  # Buy trade
            if candle['low'] <= self.stop_loss:
                self.exit_price = self.stop_loss
                return True  # Stop-loss hit
            elif candle['high'] >= self.take_profit:
                self.exit_price = self.take_profit
                return True  # Take-profit hit
        else:  # Sell trade
            if candle['high'] >= self.stop_loss:
                self.exit_price = self.stop_loss
                return True  # Stop-loss hit
            elif candle['low'] <= self.take_profit:
                self.exit_price = self.take_profit
                return True  # Take-profit hit
        return False  # Trade remains open