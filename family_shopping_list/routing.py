from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/shop/(?P<shop_name>\w+)/$", consumers.ShoppingConsumer.as_asgi()),
]