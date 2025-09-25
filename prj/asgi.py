import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.market.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.market.routing.websocket_urlpatterns
        )
    ),
})

# Binance stream **není spouštěn zde**.
# Spouštěj ho přímo ze skriptu:
# python apps/market/tasks.py
