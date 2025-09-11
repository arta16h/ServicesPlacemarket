from django.db import models
from django.conf import settings
from services.models import ProviderService
from users.models import User, Provider



class Order(models.Model):
    PAYMENT_CHOICES = [
        ("wallet", "Wallet"),
        ("cash", "Cash"),
    ]

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
        ('in_progress','In Progress'),
        ('done','Done'),
    ]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='orders')
    provider_service = models.ForeignKey(ProviderService, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey('users.Address', on_delete=models.SET_NULL, null=True, blank=True)
    address_text = models.TextField(blank=True, null=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='wallet')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    travel_fee_paid = models.BooleanField(default=False)
    service_fee_paid = models.BooleanField(default=False)
    service_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} -> {self.provider.user.username}"

class ProviderAvailability(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="availabilities")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.provider.user.username} | {self.start_time} - {self.end_time}"