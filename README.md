# Test N Bet - Trading Strategy Backtesting Platform

**"First Test. Then Bet."**

A Django-based web application for testing and analyzing cryptocurrency trading strategies through comprehensive backtesting capabilities.

## 🚀 Features

- **Trading Strategy Management**: Create, customize, and manage trading strategies
- **Backtesting Engine**: Test strategies against historical market data
- **Market Data Integration**: Real-time data from Binance and other exchanges via CCXT
- **Risk Management**: Built-in trade risk modeling and position sizing
- **User Authentication**: Secure user registration and authentication via django-allauth
- **REST API**: RESTful API endpoints for programmatic access
- **WebSocket Support**: Real-time updates using Django Channels
- **Interactive UI**: Modern interface with live reload for development

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Running Tests](#-running-tests)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠️ Tech Stack

- **Backend Framework**: Django 5.0
- **Database**: PostgreSQL with psycopg2
- **Real-time**: Django Channels 4.0, Daphne 4.0
- **Market Data**: CCXT 4.3.48, python-binance
- **Data Analysis**: pandas 2.2.0+, matplotlib
- **Authentication**: django-allauth, PyJWT
- **API**: Django REST Framework
- **Frontend**: Django Tailwind, LiveReload
- **Testing**: pytest

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12+
- PostgreSQL 16+
- pip (Python package manager)
- virtualenv (recommended)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gyarab/2025-3e-test-n-bet.git
   cd 2025-3e-test-n-bet
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Create environment file**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables**
   
   Edit `.env` and set the following variables:
   
   ```env
   # Django Settings
   SECRET_KEY=your-secret-key-here-generate-a-new-one
   DEBUG=True  # Set to False in production
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database Configuration
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_SSL=False  # Set to True if using SSL
   ```

3. **Generate a new SECRET_KEY**
   
   You can generate a secure secret key using Python:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

4. **Set up PostgreSQL database**
   
   Create a PostgreSQL database:
   ```sql
   CREATE DATABASE your_database_name;
   CREATE USER your_database_user WITH PASSWORD 'your_database_password';
   GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_database_user;
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

## 🚀 Running the Application

### Development Server

Start the Django development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### With Live Reload

For development with automatic browser refresh:
```bash
python manage.py livereload
```

### Admin Interface

Access the Django admin panel at `http://localhost:8000/admin/`

## 🧪 Running Tests

Run the test suite using Django's test runner:
```bash
python manage.py test
```

Run tests with pytest:
```bash
pytest
```

Run specific test markers:
```bash
pytest -m "not slow"  # Skip slow tests
```

## 📁 Project Structure

```
2025-3e-test-n-bet/
├── apps/
│   ├── backtests/        # Backtesting functionality
│   │   ├── services/     # Backtest engine and trade logic
│   │   ├── api/          # REST API endpoints
│   │   └── tests/        # Backtest tests
│   ├── market/           # Market data integration
│   │   ├── services.py   # Market data fetching
│   │   └── api/          # Market API endpoints
│   ├── strategies/       # Trading strategies
│   │   ├── services/     # Strategy engines and indicators
│   │   ├── api/          # Strategy API endpoints
│   │   └── tests/        # Strategy tests
│   └── registration/     # User authentication
├── core/                 # Core application views and templates
├── prj/                  # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL routing
│   ├── asgi.py           # ASGI config
│   └── wsgi.py           # WSGI config
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── pytest.ini            # Pytest configuration
└── .env.example          # Environment variables template
```

## 📚 API Documentation

### Backtests API
- `GET /api/backtests/` - List all backtests
- `POST /api/backtests/` - Create a new backtest
- `GET /api/backtests/{id}/` - Get backtest details

### Strategies API
- `GET /api/strategies/` - List all strategies
- `POST /api/strategies/` - Create a new strategy
- `GET /api/strategies/{id}/` - Get strategy details

### Market API
- `GET /api/market/` - Get market data

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- All tests pass
- Code follows the existing style
- Commit messages are clear and descriptive

## 📝 Development Guidelines

- Keep security in mind - never commit sensitive data
- Write tests for new features
- Update documentation when changing functionality
- Use environment variables for configuration
- Follow Django best practices

## 🔒 Security

- Never commit `.env` files or sensitive credentials
- Always use environment variables for secrets
- Keep `DEBUG=False` in production
- Use strong, unique `SECRET_KEY` values
- Enable SSL for database connections in production

## 📄 License

This project is part of the 2025 3E academic program.

## 👥 Authors

Developed by the 2025-3e team at Gyarab.

## 🐛 Issues

Found a bug? Please open an issue on GitHub with:
- Description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)

## 📞 Support

For support and questions, please open an issue on GitHub.

---

**Remember: First Test. Then Bet.** 🎯
