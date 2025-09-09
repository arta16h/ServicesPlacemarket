from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order
from notifications.models import Notification


# ذخیره وضعیت قبلی قبل از تغییر
@receiver(pre_save, sender=Order)
def track_old_status(sender, instance, **kwargs):
    if instance.pk:  # فقط برای سفارش‌هایی که قبلاً وجود داشتن
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None


