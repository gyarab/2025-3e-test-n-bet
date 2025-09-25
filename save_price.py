import psycopg2

conn = psycopg2.connect(
    dbname="test_n_bet",
    user="team_user",       # <--- správný uživatel
    password="tajneheslo",  # <--- jeho heslo
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Vytvoření tabulky, pokud neexistuje
cur.execute("""
CREATE TABLE IF NOT EXISTS public.btc_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    price NUMERIC(20,8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Testovací vložení
data = {"symbol": "BTCUSDT", "price": 12345.6789}
cur.execute(
    "INSERT INTO public.btc_prices (symbol, price) VALUES (%s, %s)",
    (data["symbol"], data["price"])
)
conn.commit()
print("Uloženo do DB:", data)

# Zobrazení posledních 5 řádků
cur.execute("SELECT * FROM public.btc_prices ORDER BY id DESC LIMIT 5")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
conn.close()
