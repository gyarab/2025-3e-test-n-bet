# apps/backtests/management/commands/run_backtest.py
from django.core.management.base import BaseCommand
from apps.backtests.backtest_runner import run_backtest  # <-- tady musí být "apps.backtests"

class Command(BaseCommand):
    help = "Spustí backtest pro BTC"

    def handle(self, *args, **kwargs):
        result = run_backtest()
        self.stdout.write(str(result))
