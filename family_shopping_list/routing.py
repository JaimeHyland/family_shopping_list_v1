from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/', consumers.ShoppingConsumer.as_asgi()),
]
