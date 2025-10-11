# apps/market/data_store.py

btc_prices = []  # Globální seznam ticků v paměti

def add_candle(candle):
    """Přidá nový tick do paměti"""
    btc_prices.append(candle)

def get_prices(symbol=None, limit=None):
    """Vrátí všechny tick data (nebo filtrovaná podle symbolu/limitu)"""
    data = btc_prices
    if symbol:
        data = [c for c in data if c.get('symbol') == symbol]
    if limit:
        data = data[-limit:]
    return data
