from django.db import models
from users.models import User
from orders.models import Order

class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="review")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    provider = models.ForeignKey('ProviderAvailability.provider', on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider.user.username} - {self.rating}"
