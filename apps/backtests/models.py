from django.db import models
from django.conf import settings

from apps.strategies.models import Strategy

class Asset(models.Model):
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Backtest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    initial_capital = models.FloatField(null=True, blank=True)
    position_size = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Backtest {self.id} - {self.strategy.name} on {self.asset.symbol}"
    
    
class Trade(models.Model):
    backtest = models.ForeignKey(Backtest, on_delete=models.CASCADE, related_name="trades", default=1)
    time = models.DateTimeField()
    price = models.FloatField()
    is_buy = models.BooleanField(help_text="True = BUY, False = SELL")
    quantity = models.FloatField(default=0)
    profit = models.FloatField()

    def __str__(self):
        return f"Trade {self.id} - P/L: {self.profit}"


