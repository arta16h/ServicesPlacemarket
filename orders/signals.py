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


# نوتیفیکیشن بعد از تغییر وضعیت
@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        # سفارش جدید → اطلاع به ارائه‌دهنده
        Notification.objects.create(
            user=instance.provider.user,
            message=f"سفارش جدید #{instance.id} برای شما ثبت شد."
        )
    else:
        old_status = getattr(instance, "_old_status", None)

        # فقط وقتی وضعیت تغییر کرده
        if old_status != instance.status:
            # نقش‌ها رو مدیریت می‌کنیم
            if instance.status == "accepted":
                Notification.objects.create(
                    user=instance.customer,
                    message=f"سفارش #{instance.id} توسط {instance.provider.user.full_name} تأیید شد ✅"
                )

            elif instance.status == "rejected":
                Notification.objects.create(
                    user=instance.customer,
                    message=f"متأسفانه سفارش #{instance.id} توسط {instance.provider.user.full_name} رد شد ❌"
                )

            elif instance.status == "in_progress":
                Notification.objects.create(
                    user=instance.customer,
                    message=f"سفارش #{instance.id} در حال انجام است 🛠️"
                )
                Notification.objects.create(
                    user=instance.provider.user,
                    message=f"شما سفارش #{instance.id} را آغاز کردید."
                )

            elif instance.status == "done":
                Notification.objects.create(
                    user=instance.customer,
                    message=f"سفارش #{instance.id} تکمیل شد 🎉 لطفاً نظر خود را ثبت کنید."
                )
                Notification.objects.create(
                    user=instance.provider.user,
                    message=f"شما سفارش #{instance.id} را با موفقیت تکمیل کردید 👏"
                )
