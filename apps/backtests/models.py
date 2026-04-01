from django.db import models
from django.conf import settings

from apps.strategies.models import Strategy


class Asset(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Backtest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    timeframe = models.CharField(max_length=20, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    initial_capital = models.DecimalField(max_digits=15, decimal_places=2)
    candles_amount = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    result = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Backtest {self.id} - {self.strategy.name} on {self.asset.symbol}"


class Trade(models.Model):
    backtest = models.ForeignKey(
        Backtest,
        on_delete=models.CASCADE,
        related_name="trades"
    )
    trade_type = models.CharField(max_length=10, help_text="buy or sell")
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    entry_price = models.DecimalField(max_digits=15, decimal_places=8)
    exit_price = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    stop_loss = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, help_text="open / closed")
    result = models.DecimalField(max_digits=15, decimal_places=8,null=True, blank=True, help_text="profit or loss")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trade {self.id} ({self.trade_type}) - P/L: {self.result}"
