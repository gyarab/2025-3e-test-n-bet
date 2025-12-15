from django.db import models
from django.conf import settings  # nutné pro FK na CustomUser

class Asset(models.Model):
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Backtest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField()
    price = models.FloatField()
    quantity = models.FloatField(default=0)
    profit = models.FloatField()

    def __str__(self):
        return f"Trade {self.id} - P/L: {self.profit}"
    
    
class Trade(models.Model):
    backtest = models.ForeignKey(Backtest, on_delete=models.CASCADE, related_name="trades", default=1)
    time = models.DateTimeField()
    price = models.FloatField()
    quantity = models.FloatField(default=0)
    profit = models.FloatField()

    def __str__(self):
        return f"Trade {self.id} - P/L: {self.profit}"


