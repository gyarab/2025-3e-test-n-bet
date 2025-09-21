import ccxt
from datetime import datetime

exchange = ccxt.binance({
    'enableRateLimit': True
})

def get_binance_ohlcv_and_timestamp(coin: str, interval: str, candle_amount: int = 1):
    """
    Fetch latest data for a given coin and interval from Binance using CCXT.
    
    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
        interval (str): Time interval, e.g., '1h', '1d'
        candle_amount (int): Number of candles to fetch, default is 1
        
    Returns:
        dict: Basic info (open_time, open, high, low, close, volume, close_time) for the latest {candle_amount} candles
    """

    # CCXT očekává symbol ve formátu 'BTC/USDT'
    ohlcv = exchange.fetch_ohlcv(coin.upper(), timeframe=interval, limit=candle_amount)
    if not ohlcv:
        return None
    candles = []

    for candle in ohlcv:
        candles.append({ 
            'open_time': datetime.fromtimestamp(candle[0] / 1000),
            'close_time': datetime.fromtimestamp(candle[0] / 1000 + exchange.parse_timeframe(interval) * 1000),
            'open': candle[1],
            'high': candle[2],
            'low': candle[3],
            'close': candle[4],
            'volume': candle[5]
        })
    

def get_binance_ohlcv(coin: str, interval: str, candle_amount: int = 1):
    """
    Get basic info for a coin and interval from Binance using CCXT.
    
    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
        interval (str): Time interval, e.g., '1h', '1d'
        candle_amount (int): Number of candles to fetch, default is 1
        
    Returns:
        dict: Basic info (open, close, high, low, volume) for the latest {candle_amount} candles
    """
    ohlcv_and_time = get_binance_ohlcv_and_timestamp(coin, interval, candle_amount)
    if not ohlcv_and_time:
        return None
    
    return [
        {
            'open': candle['open'],
            'close': candle['close'],
            'high': candle['high'],
            'low': candle['low'],
            'volume': candle['volume']
        }
        for candle in ohlcv_and_time
    ]

