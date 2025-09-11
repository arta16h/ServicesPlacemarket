from django.db import models
from users.models import User
from orders.models import Order
from django.conf import settings


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}: {self.balance}"
    

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("deposit", "Deposit"),       # شارژ کیف پول
        ("withdraw", "Withdraw"),     # برداشت
        ("payment", "Payment"),       # پرداخت سفارش
        ("commission", "Commission"), # کمیسیون سیستم
        ("refund", "Refund"),         # برگشت وجه
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user.username} - {self.type} - {self.amount}"


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('wallet', 'Wallet'),
        ('cash', 'Cash'),
    )
    STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    step = models.PositiveSmallIntegerField(default=1)  # مرحله پرداخت: ۱ یا ۲
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} - Step {self.step}"
