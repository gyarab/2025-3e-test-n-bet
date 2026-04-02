from django import urls
from .views import get_hot_tokens
from .views import get_candles
from .views import get_candles_in_range

urlpatterns = [
    urls.path("hot-tokens/", get_hot_tokens, name="hot-tokens"),
    urls.path("get-candles/<int:token_id>", get_candles, name="token-candles"),
    urls.path("get-candles-in-range/<int:token_id>", get_candles_in_range, name="token-candles-in-range"),
]
