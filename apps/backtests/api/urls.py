
from django.urls import path
from .views import run_backtest_view

urlpatterns = [
    path("backtest/run/", run_backtest_view, name="run-backtest"),
    
]
