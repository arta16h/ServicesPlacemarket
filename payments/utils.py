from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Wallet, Transaction

def quantize_amount(amount):
    return (Decimal(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def get_commission_rate(provider):
    total_done = provider.orders.filter(status='done').count()
    if total_done < 10:
        return Decimal('0.20')
    elif total_done < 50:
        return Decimal('0.15')
    return Decimal('0.10')


