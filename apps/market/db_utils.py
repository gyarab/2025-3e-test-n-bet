import psycopg2
from psycopg2.extras import execute_values
import json

# připojení k DB
conn = psycopg2.connect(
    dbname="test_n_bet",
    user="team_user",
    password="tajneheslo",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# funkce pro vložení ceny
def save_price(data):
    cur.execute(
        "INSERT INTO btc_prices (symbol, price) VALUES (%s, %s)",
        (data["symbol"], float(data["price"]))
    )
    conn.commit()
