from django import urls
from .views import get_hot_tokens

urlpatterns = [
    urls.path('hot-tokens/', get_hot_tokens, name='hot-tokens'),
]