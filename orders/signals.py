from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Order
from notifications.models import Notification


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
