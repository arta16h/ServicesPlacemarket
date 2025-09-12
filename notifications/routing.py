from django.urls import re_path
from . import consumers
import logging
logger = logging.getLogger(__name__)


websocket_urlpatterns = [
    re_path(r"ws/notifications/(?P<user_id>\d+)/$", consumers.NotificationConsumer.as_asgi()),
]
