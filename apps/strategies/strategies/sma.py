import ccxt
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

from apps.market.services import get_binance_ohlcv

# Inicializace Binance
exchange = ccxt.binance({
    'enableRateLimit': True
})

def calculate_sma(candles, window: int = 10):
    """
    Calculate Simple Moving Average (SMA) for the last candle from a list of OHLCV candles.

    Args:
        candles (list[dict]): List of dictionaries, each containing:
            - close
        window (int): Period for SMA (default 10)
    Returns:
        float: Latest SMA value or -1 if not enough data
    """
    if not candles or len(candles) < window:
        return -1

    # Převod na DataFrame
    df = pd.DataFrame(candles, columns=['close'])
    df['SMA'] = df['close'].rolling(window).mean()
    value = df['SMA'].iloc[-1]

    return round(float(value),3) if pd.notna(value) else -1

def get_sma_list(candles, window: int = 10):
    """
    Calculate Simple Moving Average (SMA) list from a list of OHLCV candles.

    Args:
        candles (list[dict]): List of dictionaries, each containing:
            - open, high, low, close, volume
    
        window (int): Period for SMA (default 10)
    Returns:
        list[float]: List of SMA values, with None for initial periods without enough data
    """
    if not candles or len(candles) < window:
        return []

    for candle in candles:
        if not all(k in candle for k in ('open', 'high', 'low', 'close', 'volume')):
            return []
    
    temp_candles = candles.copy()
    sma_list = []

    for i in range (len(temp_candles)):
        if not temp_candles or len(temp_candles) < window:
            sma_list.append(None)
        else:
            sma_list.append(calculate_sma(temp_candles, window))
        temp_candles = temp_candles[:-1]

    return sma_list[::-1]  # Reverzní seznam, aby odpovídal původnímu pořadí   

def get_sma_list(coin: str, interval: str, candle_amount: int = 20, window: int = 10):
    """
    Calculate Simple Moving Average (SMA) list from a list of OHLCV candles.

    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
        interval (str): Time interval, e.g., '1h', '1d'
        candle_amount (int): Number of candles to fetch, default is 20
        window (int): Period for SMA (default 10)
    Returns:
        list[float]: List of SMA values, with None for initial periods without enough data
    """
    candles = get_binance_ohlcv(coin, interval, candle_amount)
    return get_sma_list(candles, window)  

def get_sma_crossover_signal(candles, short_window: int = 10, long_window: int = 30):
    """
    Calculate SMA crossover signals from a list of OHLCV candles with timestamps.

    Args:
        candles (list[dict]): List of dictionaries, each containing:
            - open, high, low, close, volume
        short_window (int): Period for short SMA (default 10)
        long_window (int): Period for long SMA (default 30)
        
    Returns:
        str: 'BUY', 'SELL', or 'HOLD' based on the latest crossover signal. Return 'NOT ENOUGH DATA' if not enough data.
    """
    if not candles or len(candles) < long_window:
        return 'NOT ENOUGH DATA'

    SMA_short = calculate_sma(candles, short_window)
    SMA_long = calculate_sma(candles, long_window)
    
    if SMA_long is None or SMA_short is None:
        return 'NOT ENOUGH DATA'

    # Poslední hodnoty SMA
    if pd.isna(SMA_short) or pd.isna(SMA_long):
        return 'HOLD'

    if SMA_short > SMA_long:
        return 'BUY'
    elif SMA_short < SMA_long:
        return 'SELL'
    else:
        return 'HOLD'
    
def get_sma_crossover_signal(coin: str, interval: str, short_window: int = 10, long_window: int = 30):
    """
    Calculate SMA crossover signals from a list of OHLCV candles with timestamps.

    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
        interval (str): Time interval, e.g., '1h', '1d'
        short_window (int): Period for short SMA (default 10)
        long_window (int): Period for long SMA (default 30)
        
    Returns:
        str: 'BUY', 'SELL', or 'HOLD' based on the latest crossover signal. Return 'NOT ENOUGH DATA' if not enough data.
    """

    candles = get_binance_ohlcv(coin, interval, candle_amount=long_window)
    return get_sma_crossover_signal(candles, short_window, long_window)


