from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from leaderboard.models import LeaderboardSettings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"




class Provider(models.Model):
    CATEGORY_CHOICES = [
    ('cleaning', 'Cleaning'),
    ('repair', 'Repair'),
    ('beauty', 'Beauty'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provider')
    main_category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=255, blank=True)
    approved = models.BooleanField(default=False)
    documents = models.FileField(upload_to='provider_docs/', null=True, blank=True)
    total_successful_orders = models.PositiveIntegerField(default=0)
    cancel_count = models.PositiveIntegerField(default=0)
    late_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=100, blank=True)
    full_address = models.TextField()
    place_id = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.label or self.full_address[:30]}"
    

class ProviderStats(models.Model):
    provider = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stats")
    completed_orders = models.PositiveIntegerField(default=0)
    avg_rating = models.FloatField(default=0)
    final_score = models.FloatField(default=0) #امتیاز ترکیبی

    def calculate_final_score(self):
        settings_obj = LeaderboardSettings.objects.first()
        weight_orders = settings_obj.weight_orders if settings_obj else 0.7
        weight_ratings = settings_obj.weight_ratings if settings_obj else 0.3

        self.final_score = (self.completed_orders * weight_orders) + (self.avg_rating * 20 * weight_ratings)
        self.save()