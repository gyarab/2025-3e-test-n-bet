import os
import django
import asyncio
import websockets
import json
import psycopg2
from channels.layers import get_channel_layer
import sys
from pathlib import Path

# ------------------------------
# Nastavení Django
# ------------------------------
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prj.settings")
django.setup()

# ------------------------------
# Připojení k PostgreSQL
# ------------------------------
conn = psycopg2.connect(
    dbname="test_n_bet",
    user="team_user",
    password="tajneheslo",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# ------------------------------
# Funkce pro ukládání ceny
# ------------------------------
def save_price(data):
    try:
        cur.execute(
            """
            INSERT INTO btc_prices (symbol, price, created_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            """,
            (data["symbol"], float(data["price"]))
        )
        conn.commit()
        print("Uložena cena do DB:", data)
    except Exception as e:
        print("Chyba při ukládání do DB:", e)
        conn.rollback()
 # důležité, aby další příkazy šly dál

# ------------------------------
# Binance stream
# ------------------------------
async def binance_stream():
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    channel_layer = get_channel_layer()

    print("Spouštím Binance stream...")

    try:
        async with websockets.connect(url) as ws:
            print("Připojeno k Binance...")
            while True:
                try:
                    msg = await ws.recv()
                    # vypíše prvních 100 znaků zprávy
                    print("Přišla zpráva z Binance:", msg[:100], "...")

                    data = json.loads(msg)
                    price_data = {"symbol": "BTCUSDT", "price": data["p"]}
                    print("Parsed data:", price_data)

                    # Odeslání všem WebSocket klientům
                    await channel_layer.group_send(
                        "market",
                        {
                            "type": "send_price",
                            "data": price_data,
                        }
                    )
                    print("Odesláno klientům")

                    # Uložení do DB
                    save_price(price_data)

                except json.JSONDecodeError as e:
                    print("Chyba při parsování JSON:", e)
                except Exception as e:
                    print("Chyba při zpracování zprávy:", e)

    except Exception as e:
        print("Chyba při připojení k Binance:", e)

# ------------------------------
# Spuštění skriptu
# ------------------------------
if __name__ == "__main__":
    print("Spouštím Binance stream přímo ze skriptu...")
    asyncio.run(binance_stream())
