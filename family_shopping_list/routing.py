from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/', consumers.ShoppingConsumer.as_asgi()),
]