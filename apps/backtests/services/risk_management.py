from datetime import datetime, timedelta

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

def calculate_relative_stop_loss_percentage(entry_price: float, candles: list[dict], time_limit: float) -> float:
    #TODO implement relative stop loss calculation based on Average True Range (ATR) 
    pass


