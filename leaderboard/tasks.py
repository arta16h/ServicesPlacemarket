from celery import shared_task
from django.utils.timezone import now
from users.models import ProviderStats
from leaderboard.models import LeaderboardEntry
import logging
logger = logging.getLogger(__name__)


@shared_task
def calculate_monthly_leaderboard():
    # برترین‌ها را بگیر
    top_providers = ProviderStats.objects.order_by("-final_score")[:10]

    for idx, stats in enumerate(top_providers, start=1):
        LeaderboardEntry.objects.create(
            provider=stats.provider,
            rank=idx,
            completed_orders=stats.completed_orders,
            avg_rating=stats.avg_rating,
            score=stats.final_score,
            month=now().month,
            year=now().year
        )
