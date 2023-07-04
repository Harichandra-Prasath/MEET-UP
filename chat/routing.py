from django.urls import re_path

from .consumers import VideoConsumer

websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$" , VideoConsumer.as_asgi())
]   