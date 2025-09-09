from django.urls import path
from .views import NotificationListView, UnreadNotificationListView, MarkAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('unread/', UnreadNotificationListView.as_view(), name='notifications-unread'),
    path('<int:pk>/read/', MarkAsReadView.as_view(), name='notification-mark-read'),
]
