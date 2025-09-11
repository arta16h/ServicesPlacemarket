from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import Avg
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from users.models import ProviderStats
from .models import Order
from reviews.models import Review
from notifications.models import Notification
from datetime import timedelta
from django.utils.timezone import now
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json


channel_layer = get_channel_layer()
def send_order_status_change(order):
    message = f"وضعیت سفارش شما {order.id} تغییر کرد به: {order.status}"

    # ثبت در دیتابیس
    Notification.objects.create(
        user=order.customer,
        message=message
    )

    # ارسال real-time به کلاینت
    async_to_sync(channel_layer.group_send)(
        f"notifications_{order.customer.id}",
        {
            "type": "send_notification",
            "message": message,
        }
    )


def send_realtime_notification(user, message):
    notification = Notification.objects.create(
        user=user,
        message=message
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {"type": "send_notification", "message": notification.message}
    )
    send_order_status_change()

# ذخیره وضعیت قبلی قبل از تغییر
@receiver(pre_save, sender=Order)
def track_old_status(sender, instance, **kwargs):
    if instance.pk:  # فقط برای سفارش‌هایی که قبلاً وجود داشتن
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None


# نوتیفیکیشن بعد از تغییر وضعیت
@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        # سفارش جدید → اطلاع به ارائه‌دهنده
        send_realtime_notification(
            instance.provider.user,
            f"سفارش جدید #{instance.id} برای شما ثبت شد."
        )
    else:
        old_status = getattr(instance, "_old_status", None)

        # فقط وقتی وضعیت تغییر کرده
        if old_status != instance.status:
            # نقش‌ها رو مدیریت می‌کنیم
            if instance.status == "accepted":
                send_realtime_notification(
                    instance.customer,
                    f"سفارش #{instance.id} توسط {instance.provider.user.full_name} تأیید شد ✅"
                )

            elif instance.status == "rejected":
                send_realtime_notification(
                    instance.customer,
                    f"متأسفانه سفارش #{instance.id} توسط {instance.provider.user.full_name} رد شد ❌"
                )

            elif instance.status == "in_progress":
                send_realtime_notification(
                    instance.customer,
                    f"سفارش #{instance.id} در حال انجام است 🛠️"
                )
                send_realtime_notification(
                    instance.provider.user,
                    f"شما سفارش #{instance.id} را آغاز کردید."
                )

            elif instance.status == "done":
                send_realtime_notification(
                    instance.customer,
                    f"سفارش #{instance.id} تکمیل شد 🎉 لطفاً نظر خود را ثبت کنید."
                )
                send_realtime_notification(
                    instance.provider.user,
                    f"شما سفارش #{instance.id} را با موفقیت تکمیل کردید 👏"
                )


@receiver(post_save, sender=Order)
def schedule_order_reminder(sender, instance, created, **kwargs):
    if instance.status == "COMPLETED":
        # تنظیم تاریخ یادآوری (۳۰ روز بعد)
        remind_date = now() + timedelta(days=30)

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=remind_date.minute,
            hour=remind_date.hour,
            day_of_month=remind_date.day,
            month_of_year=remind_date.month,
        )

        PeriodicTask.objects.create(
            crontab=schedule,
            name=f"remind_order_{instance.id}",
            task="orders.tasks.send_order_reminder",
            args=json.dumps([instance.customer.id, instance.service.id]),
        )


@receiver(post_save, sender=Order)
def update_provider_stats_on_order(sender, instance, **kwargs):
    if instance.status == "COMPLETED":
        stats, _ = ProviderStats.objects.get_or_create(provider=instance.provider)
        stats.completed_orders += 1
        stats.calculate_final_score()

