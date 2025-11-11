from django.urls import path
from .views import get_trades

urlpatterns = [
    path('trades/', get_trades, name='get_trades'),
]
