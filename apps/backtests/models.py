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
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    initial_capital = models.DecimalField(max_digits=15, decimal_places=2)
    position_size = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    result = models.JSONField(null=True, blank=True)


    def __str__(self):
        return f"Backtest {self.id} - {self.strategy.name} on {self.asset.symbol}"
    
    
class Trade(models.Model):
    backtest = models.ForeignKey(Backtest, on_delete=models.CASCADE, related_name="trades")
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=15, decimal_places=8)
    is_buy = models.BooleanField(help_text="True = BUY, False = SELL")
    quantity = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    profit = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return f"Trade {self.id} - P/L: {self.profit}"


