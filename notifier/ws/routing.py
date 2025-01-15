from django.urls import re_path

from ws.consumers import TaskStatusConsumer

websocket_urlpatterns = [
    re_path(r"ws/tasks/$", TaskStatusConsumer.as_asgi()),
]
