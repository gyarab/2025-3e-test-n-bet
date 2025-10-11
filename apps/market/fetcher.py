# apps/market/fetcher.py
import threading
import time
from datetime import datetime
from binance.client import Client
from .data_store import add_candle

# Binance API (pro veřejná data stačí prázdné klíče)
client = Client(api_key="", api_secret="")

SYMBOL = "BTCUSDT"   # ticker, který chceme sledovat
INTERVAL = 1         # interval v sekundách

def fetch_btc_price():
    while True:
        try:
            # získání aktuální ceny
            ticker = client.get_symbol_ticker(symbol=SYMBOL)
            price = float(ticker['price'])
            
            # vytvoření ticku
            candle = {
                "symbol": "BTC",
                "price": price,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # přidání do globální paměti
            add_candle(candle)
            
        except Exception as e:
            print("Chyba při fetchi:", e)

        time.sleep(INTERVAL)

# spustí fetcher na pozadí
def start_fetcher():
    thread = threading.Thread(target=fetch_btc_price, daemon=True)
    thread.start()
