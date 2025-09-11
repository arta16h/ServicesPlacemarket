from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class LeaderboardEntry(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    completed_orders = models.PositiveIntegerField()
    avg_rating = models.FloatField()
    score = models.FloatField() 
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    class Meta:
        unique_together = ("provider", "month", "year")

    def __str__(self):
       return f"{self.provider.username} - Rank {self.rank} - Score {self.score}"
    



