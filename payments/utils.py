from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Wallet, Transaction

def quantize_amount(amount):
    return (Decimal(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


