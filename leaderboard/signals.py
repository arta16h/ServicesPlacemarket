from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import ProviderStats
from .models import LeaderboardSettings

@receiver(post_save, sender=LeaderboardSettings)
def recalculate_scores(sender, instance, **kwargs):
    for stat in ProviderStats.objects.all():
        stat.calculate_final_score()
