from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Wallet
import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)