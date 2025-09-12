from celery import shared_task
from django.contrib.auth import get_user_model
from services.models import Service
from notifications.models import Notification
import logging
logger = logging.getLogger(__name__)


User = get_user_model()

@shared_task
def send_order_reminder(user_id, service_id):
    try:
        user = User.objects.get(id=user_id)
        service = Service.objects.get(id=service_id)
        Notification.objects.create(
            user=user,
            message=f"می‌خواید دوباره سرویس {service.name} رو برای این ماه رزرو کنید؟"
        )
    except Exception as e:
        logger.exception(f"Reminder error: {e}")
