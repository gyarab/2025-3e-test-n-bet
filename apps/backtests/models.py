from django.db import models

class Asset(models.Model):
    id = models.AutoField
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name
    

class Backtest(models.Model):
    id = models.AutoField
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    strategy = models.CharField(max_length=100)
    asset = models.JSONField(default=dict, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    initial_capital = models.FloatField()
    position_size = models.FloatField()
    results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Trade(models.Model):
    id = models.AutoField
    backtest = models.ForeignKey(Backtest, on_delete=models.CASCADE, related_name='trades')
    time = models.DateTimeField()
    time = models.DateTimeField()
    price = models.FloatField()
    quantity = models.FloatField()
    profit= models.FloatField()

    def __str__(self):
        return f"Trade {self.id} - P/L: {self.profit_loss}"