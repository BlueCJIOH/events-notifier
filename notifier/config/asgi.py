import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from dotenv import load_dotenv

from django.core.asgi import get_asgi_application


dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = get_asgi_application()

from ws.middleware import JWTAuthMiddleware
from ws.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": app,
        "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
