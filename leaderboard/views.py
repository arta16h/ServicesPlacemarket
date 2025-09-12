from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LeaderboardEntry
from django.utils.timezone import now
import logging
logger = logging.getLogger(__name__)


class LeaderboardView(APIView):
    def get(self, request):
        today = now()
        leaderboard = LeaderboardEntry.objects.filter(month=today.month, year=today.year).order_by("rank")
        data = [
            {
                "provider": entry.provider.username,
                "rank": entry.rank,
                "completed_orders": entry.completed_orders,
                "avg_rating": entry.avg_rating,
                "score": entry.score,
            }
            for entry in leaderboard
        ]
        return Response(data)
