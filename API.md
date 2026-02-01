# API Documentation

## Overview

Test N Bet provides a RESTful API for programmatic access to backtesting, strategy management, and market data. All API endpoints return JSON responses.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

Currently, the API uses Django's session authentication. Future versions will support JWT tokens.

### Session Authentication

1. Login via the web interface at `/registration/login/`
2. Session cookie will be automatically included in subsequent requests
3. Include CSRF token in POST/PUT/DELETE requests

## Response Format

All API responses follow this structure:

### Success Response

```json
{
  "data": { ... },
  "status": "success"
}
```

### Error Response

```json
{
  "error": "Error message",
  "status": "error",
  "code": 400
}
```

## Backtests API

### List All Backtests

**Endpoint**: `GET /api/backtests/`

**Description**: Retrieve a list of all backtests for the authenticated user.

**Request**:
```http
GET /api/backtests/ HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "data": [
    {
      "id": 1,
      "strategy": {
        "id": 1,
        "name": "SMA Crossover"
      },
      "asset": {
        "id": 1,
        "symbol": "BTCUSDT",
        "name": "Bitcoin"
      },
      "start_date": "2024-01-01",
      "end_date": "2024-12-31",
      "initial_capital": "10000.00",
      "position_size": "0.10000000",
      "created_at": "2025-01-15T10:30:00Z",
      "result": {
        "total_trades": 25,
        "winning_trades": 15,
        "losing_trades": 10,
        "total_profit": 1250.50,
        "win_rate": 60.0,
        "max_drawdown": 8.5
      }
    }
  ],
  "status": "success"
}
```

### Create a Backtest

**Endpoint**: `POST /api/backtests/`

**Description**: Create and execute a new backtest.

**Request**:
```http
POST /api/backtests/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "strategy_id": 1,
  "asset_id": 1,
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "initial_capital": 10000.00,
  "position_size": 0.1
}
```

**Response**:
```json
{
  "data": {
    "id": 2,
    "strategy": {
      "id": 1,
      "name": "SMA Crossover"
    },
    "asset": {
      "id": 1,
      "symbol": "BTCUSDT",
      "name": "Bitcoin"
    },
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "initial_capital": "10000.00",
    "position_size": "0.10000000",
    "created_at": "2025-02-01T08:00:00Z",
    "result": null
  },
  "status": "success"
}
```

### Get Backtest Details

**Endpoint**: `GET /api/backtests/{id}/`

**Description**: Retrieve detailed information about a specific backtest.

**Request**:
```http
GET /api/backtests/1/ HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "data": {
    "id": 1,
    "strategy": {
      "id": 1,
      "name": "SMA Crossover",
      "parameters": {
        "short_period": 10,
        "long_period": 30
      }
    },
    "asset": {
      "id": 1,
      "symbol": "BTCUSDT",
      "name": "Bitcoin"
    },
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "initial_capital": "10000.00",
    "position_size": "0.10000000",
    "created_at": "2025-01-15T10:30:00Z",
    "result": {
      "total_trades": 25,
      "winning_trades": 15,
      "losing_trades": 10,
      "total_profit": 1250.50,
      "total_return": 12.51,
      "win_rate": 60.0,
      "profit_factor": 2.5,
      "max_drawdown": 8.5,
      "sharpe_ratio": 1.8
    },
    "trades": [
      {
        "id": 1,
        "time": "2024-01-05T14:30:00Z",
        "price": "42500.00",
        "is_buy": true,
        "quantity": "0.02350000",
        "profit": "0.00"
      },
      {
        "id": 2,
        "time": "2024-01-10T09:15:00Z",
        "price": "43800.00",
        "is_buy": false,
        "quantity": "0.02350000",
        "profit": "30.55"
      }
    ]
  },
  "status": "success"
}
```

## Strategies API

### List All Strategies

**Endpoint**: `GET /api/strategies/`

**Description**: Retrieve a list of all strategies available to the user.

**Request**:
```http
GET /api/strategies/ HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "data": [
    {
      "id": 1,
      "name": "SMA Crossover",
      "creator": {
        "id": 1,
        "username": "john_doe"
      },
      "base_strategy": null,
      "parameters": {
        "short_period": 10,
        "long_period": 30
      },
      "is_default": true,
      "created_at": "2025-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "name": "RSI Oversold",
      "creator": {
        "id": 1,
        "username": "john_doe"
      },
      "base_strategy": null,
      "parameters": {
        "period": 14,
        "oversold": 30,
        "overbought": 70
      },
      "is_default": false,
      "created_at": "2025-01-15T12:00:00Z"
    }
  ],
  "status": "success"
}
```

### Get Strategy Details

**Endpoint**: `GET /api/strategies/{id}/`

**Description**: Retrieve detailed information about a specific strategy.

**Request**:
```http
GET /api/strategies/1/ HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "data": {
    "id": 1,
    "name": "SMA Crossover",
    "creator": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "base_strategy": null,
    "parameters": {
      "short_period": 10,
      "long_period": 30,
      "description": "Generates buy signal when short SMA crosses above long SMA"
    },
    "is_default": true,
    "created_at": "2025-01-01T00:00:00Z"
  },
  "status": "success"
}
```

### Create a Strategy

**Endpoint**: `POST /api/strategies/`

**Description**: Create a new trading strategy.

**Request**:
```http
POST /api/strategies/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "name": "Custom MACD",
  "base_strategy_id": null,
  "parameters": {
    "fast_period": 12,
    "slow_period": 26,
    "signal_period": 9
  },
  "is_default": false
}
```

**Response**:
```json
{
  "data": {
    "id": 3,
    "name": "Custom MACD",
    "creator": {
      "id": 1,
      "username": "john_doe"
    },
    "base_strategy": null,
    "parameters": {
      "fast_period": 12,
      "slow_period": 26,
      "signal_period": 9
    },
    "is_default": false,
    "created_at": "2025-02-01T08:30:00Z"
  },
  "status": "success"
}
```

### Update a Strategy

**Endpoint**: `PUT /api/strategies/{id}/`

**Description**: Update an existing strategy.

**Request**:
```http
PUT /api/strategies/3/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "name": "Custom MACD Updated",
  "parameters": {
    "fast_period": 10,
    "slow_period": 24,
    "signal_period": 8
  }
}
```

**Response**:
```json
{
  "data": {
    "id": 3,
    "name": "Custom MACD Updated",
    "creator": {
      "id": 1,
      "username": "john_doe"
    },
    "base_strategy": null,
    "parameters": {
      "fast_period": 10,
      "slow_period": 24,
      "signal_period": 8
    },
    "is_default": false,
    "created_at": "2025-02-01T08:30:00Z"
  },
  "status": "success"
}
```

### Delete a Strategy

**Endpoint**: `DELETE /api/strategies/{id}/`

**Description**: Delete a strategy. Cannot delete default strategies.

**Request**:
```http
DELETE /api/strategies/3/ HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "message": "Strategy deleted successfully",
  "status": "success"
}
```

## Market API

### Get Market Data

**Endpoint**: `GET /api/market/`

**Description**: Retrieve current market data for supported trading pairs.

**Query Parameters**:
- `symbol` (optional): Trading pair symbol (e.g., BTCUSDT)
- `interval` (optional): Timeframe (1m, 5m, 15m, 1h, 4h, 1d)
- `limit` (optional): Number of candles to retrieve (default: 100, max: 1000)

**Request**:
```http
GET /api/market/?symbol=BTCUSDT&interval=1h&limit=100 HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "data": {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "candles": [
      {
        "timestamp": 1704110400000,
        "open": "42500.00",
        "high": "42800.00",
        "low": "42300.00",
        "close": "42650.00",
        "volume": "1250.5"
      },
      {
        "timestamp": 1704114000000,
        "open": "42650.00",
        "high": "43000.00",
        "low": "42600.00",
        "close": "42900.00",
        "volume": "1380.2"
      }
    ],
    "count": 100
  },
  "status": "success"
}
```

### Get Symbol Information

**Endpoint**: `GET /api/market/{symbol}/`

**Description**: Get detailed information about a specific trading pair.

**Request**:
```http
GET /api/market/BTCUSDT/ HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "data": {
    "symbol": "BTCUSDT",
    "name": "Bitcoin",
    "base_asset": "BTC",
    "quote_asset": "USDT",
    "current_price": "42900.00",
    "24h_change": "2.5",
    "24h_volume": "25000.00",
    "24h_high": "43500.00",
    "24h_low": "41800.00"
  },
  "status": "success"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

## Common Error Responses

### Authentication Required

```json
{
  "error": "Authentication credentials were not provided",
  "status": "error",
  "code": 401
}
```

### Resource Not Found

```json
{
  "error": "Backtest with id 999 not found",
  "status": "error",
  "code": 404
}
```

### Validation Error

```json
{
  "error": "Invalid parameters",
  "status": "error",
  "code": 400,
  "details": {
    "initial_capital": ["This field is required"],
    "start_date": ["Invalid date format"]
  }
}
```

## Rate Limiting

Currently, there are no rate limits on the API. This may change in future versions.

## WebSocket API

Test N Bet also supports WebSocket connections for real-time updates.

### Connect to WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market/');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

### Market Data Stream

**Channel**: `/ws/market/`

**Message Format**:
```json
{
  "type": "price_update",
  "symbol": "BTCUSDT",
  "price": "42900.00",
  "timestamp": 1704114000000
}
```

### Backtest Progress Stream

**Channel**: `/ws/backtest/{backtest_id}/`

**Message Format**:
```json
{
  "type": "progress_update",
  "backtest_id": 1,
  "progress": 75,
  "current_date": "2024-09-30",
  "trades_count": 18
}
```

## Best Practices

### 1. Error Handling

Always check the `status` field in responses:

```python
import requests

response = requests.get('http://localhost:8000/api/backtests/')
data = response.json()

if data.get('status') == 'success':
    backtests = data.get('data', [])
else:
    error_message = data.get('error', 'Unknown error')
    print(f"Error: {error_message}")
```

### 2. Pagination

For endpoints that return lists, implement pagination:

```python
page = 1
per_page = 50

while True:
    response = requests.get(
        'http://localhost:8000/api/backtests/',
        params={'page': page, 'per_page': per_page}
    )
    data = response.json()
    
    if not data.get('data'):
        break
    
    process_backtests(data['data'])
    page += 1
```

### 3. Asynchronous Operations

Some operations (like backtest execution) may take time. Check status periodically:

```python
# Create backtest
response = requests.post('http://localhost:8000/api/backtests/', json={
    'strategy_id': 1,
    'asset_id': 1,
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'initial_capital': 10000.00
})
backtest_id = response.json()['data']['id']

# Poll for results
import time

while True:
    response = requests.get(f'http://localhost:8000/api/backtests/{backtest_id}/')
    backtest = response.json()['data']
    
    if backtest['result']:
        print(f"Backtest complete! Results: {backtest['result']}")
        break
    
    time.sleep(5)  # Wait 5 seconds before checking again
```

## Examples

### Python Example

```python
import requests

# Base URL
BASE_URL = 'http://localhost:8000/api'

# Login first (if using session authentication)
session = requests.Session()
# ... perform login ...

# Create a strategy
strategy_data = {
    'name': 'My SMA Strategy',
    'parameters': {
        'short_period': 10,
        'long_period': 30
    }
}
response = session.post(f'{BASE_URL}/strategies/', json=strategy_data)
strategy = response.json()['data']

# Create a backtest
backtest_data = {
    'strategy_id': strategy['id'],
    'asset_id': 1,  # Bitcoin
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'initial_capital': 10000.00,
    'position_size': 0.1
}
response = session.post(f'{BASE_URL}/backtests/', json=backtest_data)
backtest = response.json()['data']

print(f"Created backtest {backtest['id']}")
```

### JavaScript Example

```javascript
const BASE_URL = 'http://localhost:8000/api';

// Create a strategy
async function createStrategy() {
    const response = await fetch(`${BASE_URL}/strategies/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        credentials: 'include',
        body: JSON.stringify({
            name: 'My RSI Strategy',
            parameters: {
                period: 14,
                oversold: 30,
                overbought: 70
            }
        })
    });
    
    const data = await response.json();
    return data.data;
}

// Get all backtests
async function getBacktests() {
    const response = await fetch(`${BASE_URL}/backtests/`, {
        credentials: 'include'
    });
    
    const data = await response.json();
    return data.data;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

## Versioning

Current API version: `v1` (implicit, no version prefix required)

Future versions will use version prefixes: `/api/v2/...`

## Support

For API support:
- Check the main [README.md](README.md) for general documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for bug reports or feature requests

---

**Last Updated**: 2026-02-01

For the most up-to-date API information, always refer to the latest version of this document.
