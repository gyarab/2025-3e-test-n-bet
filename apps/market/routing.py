from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/market/", consumers.MarketConsumer.as_asgi()),
]
