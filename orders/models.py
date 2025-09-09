from django.db import models

class Order(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    customer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='orders')
    provider = models.ForeignKey('users.ProviderProfile', on_delete=models.CASCADE, related_name='orders')
    sub_service = models.ForeignKey('services.SubCategory', on_delete=models.CASCADE)
    address = models.TextField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    initial_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Order {self.id} - {self.customer.username} -> {self.provider.user.username}"
