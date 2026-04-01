import json
import logging
from django.http import JsonResponse
from apps.strategies.models import Strategy
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from apps.backtests.services.services import run_backtest
from apps.backtests.models import Backtest, Asset, Trade

# from ccxt.base.errors import RequestTimeout

logger = logging.getLogger(__name__)


@csrf_protect
@require_http_methods(["POST"])
def run_backtest_view(request):
    """
    View to run a backtest for a given strategy.
    Expects a JSON body with the following structure:
    {
        "strategy_id": int,
        "initial_balance": float (optional, default=1000),
        "token": str (optional, default="BTC"),
        "timeframe": str (optional, default="1h"),
        "candle_amount": int (optional, default=500)
    }
    Returns a JSON response with the backtest results.
    """

    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "Authentication required"}, status=401
        )

    # Check content type
    if not request.content_type.startswith("application/json"):
        return JsonResponse(
            {"status": "error", "message": "Expected application/json"}, status=415
        )

    # Limit payload size to 1MB
    if len(request.body) > 1024 * 1024:
        return JsonResponse(
            {"status": "error", "message": "Payload too large"}, status=413
        )

    # Parse JSON body
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    # Get strategy ID from payload
    try:
        strategy_id = int(payload.get("strategy_id"))
    except (KeyError, TypeError, ValueError):
        return JsonResponse(
            {"status": "error", "message": "Invalid strategy_id"}, status=400
        )

    # Run backtest
    try:
        strategy = Strategy.objects.get(id=strategy_id)

        result = run_backtest(
            user=request.user,
            strategy=strategy,
            initial_balance=payload.get("initial_balance", 1000),
            token=payload.get("token", "BTCUSDT"),
            timeframe=payload.get("timeframe", "1h"),
            candle_amount=payload.get("candle_amount", 500),
        )
        return JsonResponse({"status": "success", "result": result})

    except Strategy.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Strategy not found"}, status=404
        )
    except Exception as e:
        logger.error(f"Error running backtest: {e}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": "Internal server error"}, status=500
        )
    except RuntimeError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=504)


logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
def save_backtest_view(request):
    """
    Docstring for save_backtest_view
    Expects a JSON body with the following structure:
    {
        "strategy_id": int,
        "token_symbol": str,
        "timeframe": str,
        "start_date": str (ISO format),
        "end_date": str (ISO format),
        "initial_capital": float,
        "candles_amount": int,
        "created_at": str (ISO format),
        "result": dict (Results from backtest run api)
    }
    Returns a JSON response with the saved backtest ID and a success message.
    """

    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "User not authenticated"}, status=401
        )

    try:
        data = json.loads(request.body)
        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        token_symbol = data.get("token_symbol")
        if (token_symbol.endswith("USDT")):
            token_symbol = token_symbol[:-4]

        asset_obj, created = Asset.objects.get_or_create(
            symbol=token_symbol, defaults={"name": token_symbol}
        )

        strategy_id = data.get("strategy_id")
        if not Strategy.objects.filter(id=strategy_id).exists():
            return JsonResponse(
                {"status": "error", "message": "Strategy not found"}, status=404
            )
        else:
            strategy_obj = Strategy.objects.get(id=strategy_id)

        start_date = data.get("start_date")
        end_date = data.get("end_date")
        created_at = data.get("created_at")

        if start_date and end_date and created_at:
            from datetime import datetime
            try:
                start_date = datetime.fromisoformat(start_date)
                end_date = datetime.fromisoformat(end_date)
                created_at = datetime.fromisoformat(created_at)
            except ValueError:
                return JsonResponse(
                    {"status": "error", "message": "Invalid time formats"}, status=400
                )
        else:
            return JsonResponse(
                {"status": "error", "message": "start_date, end_date and created_at are required"}, status=400
            )
            
        candles_amount = data.get("candles_amount")
        if candles_amount:
            try:
                candles_amount = int(candles_amount)
            except ValueError:
                return JsonResponse(
                    {"status": "error", "message": "Invalid candles_amount"}, status=400
                )
        else: 
            return JsonResponse(
                {"status": "error", "message": "candles_amount is required"}, status=400
            )
        
        timeframe = data.get("timeframe")
        if timeframe:
            if timeframe not in ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]:
                return JsonResponse(
                    {"status": "error", "message": "Invalid timeframe"}, status=400
                )
        else:
            return JsonResponse(
                {"status": "error", "message": "timeframe is required"}, status=400
            )
        
        initial_capital = data.get("initial_capital")
        if initial_capital is None:
            return JsonResponse(
                {"status": "error", "message": "initial_capital is required"}, status=400
            )

        backtest_result = {
            "final_balance": data.get("result", {}).get("final_balance"),
            "profit_loss": data.get("result", {}).get("profit_loss"),
            "total_trades": data.get("result", {}).get("total_trades"),
            "total_wins": data.get("result", {}).get("total_wins"),
            "total_losses": data.get("result", {}).get("total_losses"),
            "not_closed_trades": data.get("result", {}).get("not_closed_trades"),
        }

        backtest = Backtest.objects.create(
            user=request.user,
            strategy=strategy_obj,
            asset=asset_obj,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            candles_amount=candles_amount,
            created_at=created_at,
            result=backtest_result,
        )

        trades = [
            Trade(
                backtest=backtest,
                entry_price=t.get("entry_price"),
                exit_price=t.get("exit_price"),
                entry_time=t.get("entry_time"),
                exit_time=t.get("exit_time"),
                quantity=t.get("quantity"),
                trade_type=t.get("trade_type"),
                stop_loss=t.get("stop_loss"),
                take_profit=t.get("take_profit"),
                status=t.get("status"),
                result=t.get("result"),
            )
            for t in data.get("result", {}).get("trades", [])
        ]

        Trade.objects.bulk_create(trades)

        return JsonResponse(
            {
                "status": "success",
                "backtest_id": backtest.id,
                "message": "Backtest successfully saved",
            },
            status=201,
        )

    except Exception as err:
        logger.error(f"Error saving backtest: {err}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"Error: {str(err)}"}, status=500
        )


@require_http_methods(["GET"])
def get_user_backtest(request):
    """
    Retrieves backtests filtered by user_id if provided.
    """

    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "Authentication required"}, status=401
        )

    user = request.user

    try:
        backtests = Backtest.objects.filter(user=user)

        data = [
            {
                "id": b.id,
                "user_id": b.user.id,
                "strategy": {
                    "id": b.strategy_id,
                    "name": b.strategy.name,
                    "parameters": b.strategy.parameters,
                },
                "asset": {
                    "id": b.asset_id,
                    "symbol": b.asset.symbol,
                    "name": b.asset.name,
                },
                "start_date": b.start_date.isoformat() if b.start_date else None,
                "end_date": b.end_date.isoformat() if b.end_date else None,
                "initial_capital": b.initial_capital,
                "created_at": b.created_at.isoformat() if b.created_at else None,
                "trades": [
                    {
                        "id": t.id,
                        "time": t.time.isoformat(),
                        "price": t.price,
                        "quantity": t.quantity,
                        "profit": t.profit,
                        "type": "BUY" if t.is_buy else "SELL",
                    }
                    for t in b.trades.all()
                ],
            }
            for b in backtests
        ]

        return JsonResponse({"status": "success", "backtests": data})

    except Exception as e:
        logger.error(f"Error retrieving strategies: {e}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": "Internal server error"}, status=500
        )
