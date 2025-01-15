import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application

from notifier.utils.initializer import app_initializer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notifier.settings")

app_initializer.initialize_clickhouse_logger()

app = get_asgi_application()

from ws.middleware import JWTAuthMiddleware
from ws.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": app,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
