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
    

class LeaderboardSettings(models.Model):
    weight_orders = models.FloatField(default=0.7, help_text="وزن تعداد سفارش‌ها (بین 0 و 1)")
    weight_ratings = models.FloatField(default=0.3, help_text="وزن امتیاز (بین 0 و 1)")

    def clean(self):
        if (self.weight_orders + self.weight_ratings) != 1:
            raise ValidationError("جمع وزن‌ها باید برابر با 1 باشد.")

    def __str__(self):
        return "تنظیمات امتیازدهی لیدربورد"

    class Meta:
        verbose_name = "تنظیمات لیدربورد"
        verbose_name_plural = "تنظیمات لیدربورد"

