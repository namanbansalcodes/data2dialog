
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data2dialog.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    )
})
