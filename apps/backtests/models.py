from django.db import models

class BacktestPrice(models.Model):
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField()  # už to máš v DB

    class Meta:
        db_table = 'btc_prices'  # důležité, aby používal tu stávající tabulku
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.symbol} - {self.price} ({self.timestamp})"
    

class Backtest(models.Model):
    pass

class Trade(models.Model):
    pass