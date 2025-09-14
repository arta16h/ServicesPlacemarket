from django.urls import path
from .views import NotificationListView, UnreadNotificationListView, MarkNotificationReadView
import logging
logger = logging.getLogger(__name__)


urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('unread/', UnreadNotificationListView.as_view(), name='notifications-unread'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
]
