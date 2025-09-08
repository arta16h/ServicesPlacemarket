from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_category = models.CharField(max_length=50, choices=[
        ("cleaning", "Cleaning"),
        ("repair", "Repair"),
        ("beauty", "Beauty"),
    ])
    service_area = models.CharField(max_length=255)
    document = models.FileField(upload_to="documents/", null=True, blank=True)