# Project Architecture

## Overview

Test N Bet is a Django-based trading strategy backtesting platform designed with a modular architecture that separates concerns into distinct applications and services.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                   (Templates + Static)                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────┐
│                       Django Core                            │
│                                                               │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │    URLs    │  │  Middleware  │  │   Authentication    │ │
│  └────────────┘  └──────────────┘  └─────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐ ┌───────▼────────┐ ┌───────▼────────┐
│   Backtests    │ │   Strategies   │ │     Market     │
│      App       │ │      App       │ │      App       │
│                │ │                │ │                │
│ ┌────────────┐ │ │ ┌────────────┐ │ │ ┌────────────┐ │
│ │   Models   │ │ │ │   Models   │ │ │ │   Models   │ │
│ └────────────┘ │ │ └────────────┘ │ │ └────────────┘ │
│ ┌────────────┐ │ │ ┌────────────┐ │ │ ┌────────────┐ │
│ │   Views    │ │ │ │   Views    │ │ │ │  Services  │ │
│ └────────────┘ │ │ └────────────┘ │ │ └────────────┘ │
│ ┌────────────┐ │ │ ┌────────────┐ │ │                │
│ │  Services  │ │ │ │  Services  │ │ │                │
│ └────────────┘ │ │ └────────────┘ │ │                │
│ ┌────────────┐ │ │ ┌────────────┐ │ │                │
│ │    API     │ │ │ │    API     │ │ │                │
│ └────────────┘ │ │ └────────────┘ │ │                │
└────────────────┘ └────────────────┘ └────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                ┌───────────▼───────────┐
                │    PostgreSQL DB      │
                └───────────────────────┘
```

## Core Components

### 1. Django Project (prj/)

**Purpose**: Central configuration and routing

**Key Files**:
- `settings.py`: Django settings with environment variable support
- `urls.py`: Main URL routing configuration
- `asgi.py`: ASGI configuration for WebSocket support
- `wsgi.py`: WSGI configuration for HTTP server

**Responsibilities**:
- Environment configuration
- Database settings
- Middleware configuration
- URL routing to apps

### 2. Core App

**Purpose**: Base application functionality

**Components**:
- Homepage views and templates
- Static files organization
- Base templates and layouts

### 3. Backtests App

**Purpose**: Manage and execute strategy backtests

**Structure**:
```
apps/backtests/
├── models.py           # Backtest, Asset, Trade models
├── views.py            # Web views for backtest pages
├── services/
│   ├── backtest/
│   │   ├── backtest_engine.py  # Main backtesting logic
│   │   └── trade_engine.py     # Trade execution simulation
│   └── services.py     # Service layer functions
├── api/
│   ├── views.py        # REST API endpoints
│   └── urls.py         # API URL routing
└── tests/              # Unit and integration tests
```

**Key Features**:
- Backtest execution engine
- Trade simulation and tracking
- Historical data analysis
- Performance metrics calculation

**Models**:
- `Backtest`: Stores backtest configuration and results
- `Asset`: Trading pair/symbol information
- `Trade`: Individual trade records from backtests

### 4. Strategies App

**Purpose**: Define and manage trading strategies

**Structure**:
```
apps/strategies/
├── models.py           # Strategy model
├── views.py            # Strategy management views
├── services/
│   ├── core/
│   │   ├── strategy_engine.py      # Base strategy engine
│   │   └── trade_risk_model.py     # Risk management
│   ├── indicators/     # Technical indicators
│   └── atomic_strategies/  # Individual strategy implementations
├── api/
│   ├── views.py        # REST API endpoints
│   └── urls.py         # API URL routing
└── tests/              # Strategy tests
```

**Key Features**:
- Strategy creation and customization
- Technical indicator library
- Signal generation
- Parameter optimization

**Models**:
- `Strategy`: Strategy configuration and parameters

**Strategy Types**:
- Moving Average (SMA, EMA)
- MACD (Moving Average Convergence Divergence)
- RSI (Relative Strength Index)
- Custom strategies with JSON parameters

### 5. Market App

**Purpose**: Market data acquisition and management

**Structure**:
```
apps/market/
├── models.py           # Market data models
├── services.py         # Data fetching services
├── api/
│   ├── views.py        # Market data API
│   └── urls.py         # API URL routing
└── views.py
```

**Key Features**:
- Integration with Binance API
- CCXT library for multiple exchanges
- Historical OHLCV data retrieval
- Real-time price updates

**Data Sources**:
- Binance via python-binance
- Multiple exchanges via CCXT
- WebSocket connections for real-time data

### 6. Registration App

**Purpose**: User authentication and management

**Components**:
- Custom user model
- Authentication views
- Integration with django-allauth
- Google OAuth support

## Data Flow

### Backtest Execution Flow

```
1. User creates/selects strategy
   ↓
2. User configures backtest parameters
   ↓
3. System fetches historical market data
   ↓
4. BacktestEngine initializes with strategy
   ↓
5. Engine iterates through candles
   ↓
6. Strategy generates signals (BUY/SELL/HOLD)
   ↓
7. TradeEngine executes virtual trades
   ↓
8. Risk model manages position sizing
   ↓
9. Results stored in database
   ↓
10. Performance metrics displayed to user
```

### Strategy Signal Generation

```
Market Data (OHLCV)
   ↓
Technical Indicators (SMA, RSI, MACD, etc.)
   ↓
Strategy Logic (Custom algorithms)
   ↓
Signal (BUY/SELL/HOLD)
   ↓
Risk Management (Position sizing, stop loss)
   ↓
Trade Execution
```

## Database Schema

### Core Tables

**strategies_strategy**
- `id`: Primary key
- `name`: Strategy name
- `creator_id`: Foreign key to user
- `base_strategy_id`: Self-referencing for strategy inheritance
- `parameters`: JSON field for strategy configuration
- `is_default`: Boolean flag
- `created_at`: Timestamp

**backtests_backtest**
- `id`: Primary key
- `user_id`: Foreign key to user
- `strategy_id`: Foreign key to strategy
- `asset_id`: Foreign key to asset
- `start_date`: Backtest start date
- `end_date`: Backtest end date
- `initial_capital`: Starting capital
- `position_size`: Position sizing
- `created_at`: Timestamp
- `result`: JSON field for results

**backtests_trade**
- `id`: Primary key
- `backtest_id`: Foreign key to backtest
- `time`: Trade execution time
- `price`: Trade price
- `is_buy`: Boolean (True=BUY, False=SELL)
- `quantity`: Trade quantity
- `profit`: Profit/loss for this trade

**backtests_asset**
- `id`: Primary key
- `symbol`: Unique trading symbol
- `name`: Asset name

## API Architecture

### REST API Endpoints

**Backtests**
- `GET /api/backtests/` - List backtests
- `POST /api/backtests/` - Create backtest
- `GET /api/backtests/{id}/` - Get backtest details

**Strategies**
- `GET /api/strategies/` - List strategies
- `POST /api/strategies/` - Create strategy
- `GET /api/strategies/{id}/` - Get strategy details
- `PUT /api/strategies/{id}/` - Update strategy
- `DELETE /api/strategies/{id}/` - Delete strategy

**Market**
- `GET /api/market/` - Get market data
- `GET /api/market/{symbol}/` - Get symbol data

### WebSocket Support

Using Django Channels for real-time updates:
- Live market price updates
- Backtest progress notifications
- Real-time trade alerts

## Security Architecture

### Environment Variables

All sensitive configuration stored in `.env`:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode flag
- `DB_PASSWORD`: Database password
- API keys and tokens

### Authentication

- Django's built-in auth system
- django-allauth for OAuth
- JWT tokens for API authentication
- CSRF protection enabled

### Database Security

- SSL/TLS connections supported
- Password validators enforced
- SQL injection protection via ORM
- Parameterized queries

## Testing Strategy

### Test Structure

```
apps/backtests/tests/
├── test_backtest.py              # Backtest engine tests
├── test_sma_backtest.py          # SMA strategy tests
├── trade_test.py                 # Trade execution tests
└── trade_risk_management_test.py # Risk management tests

apps/strategies/tests/
├── strategy_test.py              # Base strategy tests
├── sma_test.py                   # SMA indicator tests
├── rsi_test.py                   # RSI indicator tests
└── macd_test.py                  # MACD indicator tests
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: Multi-component interaction
- **API Tests**: REST endpoint testing
- **Slow Tests**: Market data fetching, long-running backtests

## Performance Considerations

### Optimization Strategies

1. **Database**
   - Indexed foreign keys
   - JSON fields for flexible data storage
   - Connection pooling

2. **Caching**
   - Django's cache framework
   - Channel layers for WebSocket state

3. **Data Processing**
   - Pandas for efficient data manipulation
   - Batch processing for historical data
   - Lazy loading for large datasets

## Deployment Architecture

### Development
- SQLite or local PostgreSQL
- Django development server
- DEBUG=True
- Live reload enabled

### Production
- PostgreSQL with SSL
- Gunicorn/Daphne WSGI/ASGI server
- Nginx reverse proxy
- DEBUG=False
- Static files served via CDN

## Future Enhancements

### Planned Features

1. **Advanced Strategies**
   - Machine learning integration
   - Multi-timeframe analysis
   - Portfolio optimization

2. **Real-time Trading**
   - Live trading execution
   - Paper trading mode
   - Order management

3. **Analytics**
   - Advanced performance metrics
   - Risk analysis tools
   - Comparative analytics

4. **Collaboration**
   - Strategy sharing
   - Community ratings
   - Discussion forums

## Technology Choices

### Why Django?
- Mature ORM for complex data relationships
- Built-in admin interface
- Strong security features
- Rich ecosystem

### Why PostgreSQL?
- JSONB support for flexible data storage
- Advanced indexing capabilities
- Reliable and scalable
- Strong data integrity

### Why Channels?
- Real-time WebSocket support
- Integration with Django
- Scalable channel layers
- ASGI support

### Why CCXT?
- Unified API for multiple exchanges
- Active maintenance
- Comprehensive documentation
- Battle-tested

## Maintenance and Monitoring

### Health Checks
- Database connectivity
- API availability
- WebSocket connections
- External service dependencies

### Logging
- Django logging framework
- Error tracking
- Performance monitoring
- Audit trails

## Documentation Standards

### Code Documentation
- Docstrings for all public functions
- Type hints where applicable
- Inline comments for complex logic
- README files in each app

### API Documentation
- Endpoint descriptions
- Request/response examples
- Authentication requirements
- Error codes and handling

---

**Last Updated**: 2026-02-01

For questions or clarifications, please refer to the main README.md or open an issue.
