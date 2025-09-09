from django.db import models
from users.models import User
from orders.models import Order


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"اعتبار کیف پول ({self.user.username}): {self.balance}"
    

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
