import ccxt
from datetime import datetime

exchange = ccxt.binance({"enableRateLimit": True})


def get_binance_ohlcv_and_timestamp(coin: str, interval: str, candle_amount: int = 500, start_date: str = None):
    """
    Fetch latest data for a given coin and interval from Binance using CCXT.

    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
        interval (str): Time interval, e.g., '1h', '1d'
        candle_amount (int): Number of candles to fetch, default is 500
        start_date (str): Optional start date in ISO format, e.g., '2023-01-01T00:00:00Z'. If not provided, fetches the most recent candles.

    Returns:
        dict: Basic info (open_time, open, high, low, close, volume, close_time) for the latest {candle_amount} candles
    """
    coin = format_coin_symbol(coin)
    
    if candle_amount:
        try:
            candle_amount = int(candle_amount)
        except ValueError:
            candle_amount = 500

    since = None
    if start_date:
        since = int(start_date.timestamp() * 1000)
    
    ohlcv = exchange.fetch_ohlcv(
        coin.upper(), timeframe=interval, since=since, limit=int(candle_amount)
    )

    if not ohlcv:
        return None
    candles = []

    for candle in ohlcv:
        candles.append(
            {
                "open_time": datetime.fromtimestamp(candle[0] / 1000),
                "close_time": datetime.fromtimestamp(
                    candle[0] / 1000 + exchange.parse_timeframe(interval) * 1000
                ),
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5],
            }
        )

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
            "open": candle["open"],
            "close": candle["close"],
            "high": candle["high"],
            "low": candle["low"],
            "volume": candle["volume"],
        }
        for candle in ohlcv_and_time
    ]


def get_binance_ohlcv_range(coin: str, interval: str, start_date: str, end_date: str):
    """
    Get OHLCV data for a coin and interval from Binance using CCXT within a specified date range.
    
    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
        interval (str): Time interval, e.g., '1h', '1d'
        start_date (str): Start date in ISO format, e.g., '2023-01-01T00:00:00Z'
        end_date (str): End date in ISO format, e.g., '2023-01-31T23:59:59Z'

    Returns:
        list: List of OHLCV data points within the specified date range
    """
    coin = format_coin_symbol(coin)

    since = int(start_date.timestamp() * 1000)
    all_candles = []

    # Binance API returns a maximum of 1000 candles per request, so we need to loop until we get all candles in the specified date range
    while True:
        ohlcv = exchange.fetch_ohlcv(coin.upper(), timeframe=interval, since=since, limit=1000)

        if not ohlcv:
            break

        for candle in ohlcv:
            candle_time = candle[0]

            if candle_time > int(end_date.timestamp() * 1000):
                return all_candles

            all_candles.append(candle)

        since = ohlcv[-1][0] + 1  # move forward

    return all_candles


def format_coin_symbol(coin: str):
    """
    Format a coin symbol to match Binance's format (e.g., 'BTCUSDT').

    Args:
        coin (str): Coin symbol, e.g., 'BTC/USDT', 'BTCUSDT', 'BTC' etc.

    Returns:
        str: Formatted coin symbol, e.g., 'BTC/USDT'
    """
    if not coin.endswith("USDT") and not coin.endswith("USDC") and not coin.endswith("BUSD"):
        return f"{coin.upper()}/USDT"
    
    return coin.upper() if "/" in coin else f"{coin.upper()[:-4]}/USDT"


def calculate_start_and_end_dates(candles: list[dict]):
    """
    Calculate the start and end dates from a list of candles.

    Args:
        candles (list[dict]): List of candles, each containing 'open_time' and 'close_time' keys.

    Returns:
        tuple: A tuple containing the start date and end date as datetime objects.
    """
    if not candles:
        return None, None

    start_date = min(candle["open_time"] for candle in candles)
    end_date = max(candle["close_time"] for candle in candles)

    return start_date, end_date


def get_live_binance_price(coin: str):
    """
    Get the current price of a coin from Binance using CCXT.

    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
    Returns:
        float: Current price of the coin
    """
    ticker = exchange.fetch_ticker(coin.upper())
    return ticker["last"] if "last" in ticker else None


def get_live_binance_change(coin: str):
    """
    Get the 24-hour price change of a coin from Binance using CCXT.

    Args:
        coin (str): Symbol, e.g., 'BTC/USDT'
    Returns:
        float: 24-hour price change of the coin
    """
    ticker = exchange.fetch_ticker(coin.upper())
    return ticker["change"] if "change" in ticker else None


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
            "current_price": ticker["last"] if "last" in ticker else None,
            "24h_change": ticker["change"] if "change" in ticker else None,
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


def get_hot_coins(
    threshold_change: float = 5.0, only_positive: bool = False, limit: int = 10
):
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

    if not markets:
        return hot_coins

    # Filter to only USDT pairs
    markets = {k: v for k, v in markets.items() if k.endswith("/USDT")}

    for ticker, value in markets.items():
        if "percentage" in value:
            if value["percentage"] is None:
                continue

            market = exchange.markets[ticker]
            spot_url = None

            if not market.get("active", False):
                continue

            if "spot" in market and market["spot"]:
                base = market["base"] if "base" in market else "BTC"
                quote = market["quote"] if "quote" in market else "USDT"
                spot_url = f"https://www.binance.com/en/trade/{base}_{quote}?type=spot"
            else:
                continue

            if (only_positive and value["percentage"] >= threshold_change) or (
                not only_positive and value["percentage"] <= -threshold_change
            ):
                hot_coins.append(
                    {
                        "symbol": ticker,
                        "current_price": value["last"] if "last" in value else None,
                        "24h_change": (
                            value["percentage"] if "percentage" in value else None
                        ),
                        "volume": (
                            value["baseVolume"] if "baseVolume" in value else None
                        ),
                        "spot_url": spot_url if spot_url else None,
                    }
                )

    hot_coins = sorted(hot_coins, key=lambda x: x["24h_change"], reverse=only_positive)[
        :limit
    ]

    return hot_coins
