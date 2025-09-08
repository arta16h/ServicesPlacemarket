from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_customer = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    default_address = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.username} ({'provider' if self.is_provider else 'customer' if self.is_customer else 'user'})"




class ProviderProfile(models.Model):
    CATEGORY_CHOICES = [
    ('cleaning', 'Cleaning'),
    ('repair', 'Repair'),
    ('beauty', 'Beauty'),
    ]
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    main_category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, null=True, blank=True)
    service_area = models.CharField(max_length=255, blank=True, null=True)
    document = models.FileField(upload_to='provider_docs/', blank=True, null=True)
    verified = models.BooleanField(default=False)
    total_successful_orders = models.PositiveIntegerField(default=0)
    cancel_count = models.PositiveIntegerField(default=0)
    late_count = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"ProviderProfile: {self.user.username}"