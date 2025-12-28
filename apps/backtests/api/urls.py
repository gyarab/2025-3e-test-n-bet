
from django.urls import path
from .views import run_backtest_view, get_user_backtest

urlpatterns = [
    path("run/", run_backtest_view, name="run_backtest"), # Endpoint to run a backtest
    path('get/', get_user_backtest, name='user_backtests'), # Endpoint to get user's backtests
]
