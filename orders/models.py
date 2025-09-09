from django.db import models
from services.models import ProviderService
from users.models import User, ProviderProfile



class Order(models.Model):
    PAYMENT_CHOICES = [
        ("wallet", "Wallet"),
        ("cash", "Cash"),
    ]

    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="orders")
    service = models.ForeignKey(ProviderService, on_delete=models.CASCADE, related_name="orders")
    address = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} → {self.provider.user.username} ({self.service.subcategory.name})"


class ProviderAvailability(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="availabilities")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.provider.user.username} - {self.date} {self.start_time}-{self.end_time}"