# apps/backtests/backtest_runner.py
from apps.backtests.models import BacktestPrice

def run_backtest(symbol="BTCUSDT"):
    """
    Spustí backtest na historických datech z databáze.
    """
    # Načteme ceny z DB
    prices = BacktestPrice.objects.filter(symbol=symbol).order_by('timestamp')
    
    # Příklad jednoduché simulace: počítáme zisk, pokud cena vzroste
    result = {
        "symbol": symbol,
        "total_ticks": prices.count(),
        "trades": [],
        "profit": 0
    }
    
    last_price = None
    for p in prices:
        if last_price:
            if p.price > last_price:
                result["trades"].append({"action": "buy", "price": float(p.price), "timestamp": p.timestamp})
                result["profit"] += float(p.price - last_price)
        last_price = p.price

    return result
