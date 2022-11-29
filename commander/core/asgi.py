import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import apps.chat.routing
import apps.stingray.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            # URLRouter(apps.chat.routing.websocket_urlpatterns)
            URLRouter(apps.stingray.routing.websocket_urlpatterns)
        ),
    }
)
