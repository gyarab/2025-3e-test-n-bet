from django.apps import AppConfig

class MarketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.market'

    def ready(self):
        # spustíme fetcher při startu aplikace
        from .fetcher import start_fetcher
        start_fetcher()
