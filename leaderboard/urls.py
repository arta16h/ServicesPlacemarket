from django.urls import path
from .views import LeaderboardView
import logging
logger = logging.getLogger(__name__)


urlpatterns = [
    path("", LeaderboardView.as_view(), name="leaderboard"),
]
