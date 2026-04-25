# First Test. Then Bet.

A Django-based web application for designing, testing, and evaluating custom crypto trading strategies.

> Originally developed as a school project at Gymnázium, Praha 6, Arabská 14.


## Main features
- Build simple strategies using:
    - SMA (Simple Moving Average)
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence)
- Combine multiple indicators into custom strategies
- Configure indicator parameters (e.g. SMA windows, RSI thresholds)
- Run backtests on historical data from Binance exchange
    - _Currently supports only 3 cryptocurrencies, but can be simply updated to all binance-listed tokens._
- Visualize trades directly on price charts

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/first-test-then-bet.git
cd first-test-then-bet
```

---

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment setup

This project uses `django-environ` to load environment variables from a `.env` file.

```bash
cp .env.example .env
```


#### Generate a SECRET_KEY

Generate a secure Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then paste it into your `.env` file:

```env
SECRET_KEY=your-generated-key
```

---

Update the values as needed:

| Variable    | Description                  | Default   |
| ----------- | ---------------------------- | --------- |
| DB_NAME     | PostgreSQL database name     | your_db   |
| DB_USER     | Database user                | postgres  |
| DB_PASSWORD | Database password            | postgres  |
| DB_HOST     | Database host                | localhost |
| DB_PORT     | Database port                | 5432      |
| DB_SSL      | Enable SSL for DB connection | False     |
| DEBUG       | Django debug mode            | True      |
| SECRET_KEY  | Django secret key            | changeme  |


---

### 5. Apply migrations 

```bash
python manage.py migrate
```

---

### 6. Load initial data

Loaded default strategies like this:

```bash
python manage.py laoddata apps/strategies/fixtures/strategies.json
```

---

### 7. Run the development server

```bash
python manage.py runserver
```

---

## Tech Stack

| Layer       | Technology |
|-------------|-----------|
| Backend     | Django (Python) |
| API         | Custom Django JSON API with manual serialization |
| Database    | PostgreSQL |
| Frontend    | HTML, CSS, JavaScript, Tailwind CSS |
| Data Source | Binance API |


---

## Notes

* Ensure PostgreSQL is running and the database exists
* `.env` is required for the project to start

---
