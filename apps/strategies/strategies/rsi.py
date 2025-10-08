import ccxt
import pandas as pd

from apps.market.services import get_binance_ohlcv

# Inicializace Binance
exchange = ccxt.binance({
    'enableRateLimit': True
})

def calculate_rsi(candles, period: int = 14):
    """
    Calculate Relative Strength Index (RSI) for the last candle from a list of OHLCV candles.

    Args:
        candles (list[dict]): List of dictionaries, each containing:
            - close
        period (int): Period for RSI (default 14)
    Returns:
        float: Latest RSI value or -1 if not enough data
    """
    if not candles or len(candles) < period:
        return -1

    delta = candles['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = (100 - (100 / (1 + rs))).iloc[-1]

    return round(float(rsi),3) if pd.notna(rsi) else -1

def get_rsi_list(candles, period: int = 14):
    """
    Calculate Relative Strength Index (RSI) list from a list of OHLCV candles.

    Args:
        candles (list[dict]): List of dictionaries, each containing:
            - open, high, low, close, volume
    
        period (int): Period for RSI (default 14)
    Returns:
        list[float]: List of RSI values, with None for initial periods without enough data
    """
    if not candles or len(candles) < period:
        return []

    for candle in candles:
        if not all(k in candle for k in ('open', 'high', 'low', 'close', 'volume')):
            return []
    
    temp_candles = candles.copy()
    rsi_list = []

    for i in range (len(temp_candles)):
        if not temp_candles or len(temp_candles) < period:
            rsi_list.append(None)
        else:
            rsi_list.append(calculate_rsi(temp_candles, period))
        temp_candles = temp_candles[:-1]

    return rsi_list[::-1]  # Reverzní seznam, aby odpovídal původnímu pořadí   

def get_rsi_list(coin: str, interval: str, candle_amount: int = 20, period: int = 14):
    """
    Calculate Relative Strength Index (RSI) list from a list of OHLCV candles.

    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
        interval (str): Time interval, e.g., '1h', '1d'
        candle_amount (int): Number of candles to fetch, default is 20
        period (int): Period for RSI (default 14)
    Returns:
        list[float]: List of RSI values, with None for initial periods without enough data
    """
    candles = get_binance_ohlcv(coin, interval, candle_amount)
    return get_rsi_list(candles, period)  

def get_rsi_crossover_signal(candles, period: int = 14, oversold: int = 30, overbought: int = 70):
    """
    Calculate RSI signals from a list of OHLCV candles with timestamps.

    Args:
        candles (list[dict]): List of dictionaries, each containing:
            - open, high, low, close, volume
        period (int): Period for short RSI (default 14)
        oversold (int): RSI value below which we buy (default 30)
        overbought (int): RSI value above which we sell (default 70)
        
    Returns:
        str: 'BUY', 'SELL', or 'HOLD' based on the latest crossover signal. Return 'NOT ENOUGH DATA' if not enough data.
    """
    if not candles or len(candles) < period:
        return 'NOT ENOUGH DATA'

    RSI = calculate_rsi(candles, period)
    
    if RSI is None:
        return 'NOT ENOUGH DATA'

    # Poslední hodnoty SMA
    if pd.isna(RSI):
        return 'HOLD'
    elif RSI < oversold:
        return 'BUY'
    elif RSI > overbought:
        return 'SELL'
    else:
        return 'HOLD'
    
def get_rsi_crossover_signal(coin: str, interval: str, period: int = 14, oversold: int = 30, overbought: int = 70):
    """
    Calculate RSI signal from a list of OHLCV candles with timestamps.

    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
        interval (str): Time interval, e.g., '1h', '1d'
        period (int): Period for short RSI (default 14)
        oversold (int): RSI value below which we buy (default 30)
        overbought (int): RSI value above which we sell (default 70)
        
    Returns:
        str: 'BUY', 'SELL', or 'HOLD' based on the latest rsi signal. Return 'NOT ENOUGH DATA' if not enough data.
    """

    candles = get_binance_ohlcv(coin, interval, candle_amount=long_window)
    return get_rsi_crossover_signal(candles, period, oversold, overbought)
