from django.apps import AppConfig
import logging


class LeaderboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leaderboard'

    def ready(self):
        import leaderboard.signals

logger = logging.getLogger(__name__)
