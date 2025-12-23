
from django.urls import path
from .views import run_backtest_view

urlpatterns = [
    path("/run/", run_backtest_view, name="run_backtest"),
]
