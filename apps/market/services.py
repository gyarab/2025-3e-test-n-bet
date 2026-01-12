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
    ohlcv = exchange.fetch_ohlcv(coin.upper(), timeframe=interval, limit=int(candle_amount))
    print("Length of ohlcv fetched:", len(ohlcv))
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

    return candles
    

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

def get_live_binance_price(coin: str):
    """
    Get the current price of a coin from Binance using CCXT.
    
    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
    Returns:
        float: Current price of the coin
    """
    ticker = exchange.fetch_ticker(coin.upper())
    return ticker['last'] if 'last' in ticker else None

def get_live_binance_change(coin: str):
    """
    Get the 24-hour price change of a coin from Binance using CCXT.
    
    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
    Returns:
        float: 24-hour price change of the coin
    """
    ticker = exchange.fetch_ticker(coin.upper())
    return ticker['change'] if 'change' in ticker else None

def get_market_summary(coin_list: list[str]):
    """
    Get market summary for a list of coins from Binance using CCXT.
    
    Args:
        coin_list (list[str]): List of symbols, e.g., ['BTC/USDT', 'ETH/USDT']
    
    Returns:
        dict: Market summary including current price and 24-hour change for each coin
    """
    summary = {}
    for coin in coin_list:
        ticker = exchange.fetch_ticker(coin.upper())
        summary[coin] = {
            'current_price': ticker['last'] if 'last' in ticker else None,
            '24h_change': ticker['change'] if 'change' in ticker else None
        }
    return summary

def get_supported_binance_symbols():
    """
    Get a list of all supported trading pairs (symbols) on Binance using CCXT.
    
    Returns:
        list: List of supported trading pairs
    """
    markets = exchange.load_markets()
    return list(markets.keys())

def get_hot_coins(threshold_change: float = 5.0, only_positive: bool = False, limit: int = 10):
    """
    Get a list of 'hot' coins from Binance using CCXT, defined as those with a 24-hour change above a certain threshold.
    
    Args:
        threshold_change (float): Minimum 24-hour change percentage to consider a coin 'hot'
        positive (bool): If True, only consider coins with positive changes. Otherwise, consider only negative changes.
    
    Returns:
        list: List of hot coins with their current price, 24-hour change, and volume
    """
    hot_coins = []
    markets = exchange.fetch_tickers()

    print(markets)

    if not markets:
        return hot_coins

    # Filter to only USDT pairs
    for m in list(markets.keys()):
        if not m.endswith('/USDT'):
            del markets[m]
    
    for symbol in markets.keys():
        ticker = exchange.fetch_ticker(symbol)
        if 'change' in ticker:
            if (ticker['change'] is None):
                continue
            print(f"Evaluating {symbol}: change = {ticker['change']}")
            if (only_positive and ticker['change'] >= threshold_change) or (not only_positive and ticker['change'] <= -threshold_change):
                hot_coins.append({
                    'symbol': symbol,
                    'current_price': ticker['last'] if 'last' in ticker else None,
                    '24h_change': ticker['change'],
                    'volume': ticker['baseVolume'] if 'baseVolume' in ticker else None
                })

    hot_coins = sorted(hot_coins, key=lambda x: x['24h_change'], reverse=only_positive)[:limit]

    return hot_coins
