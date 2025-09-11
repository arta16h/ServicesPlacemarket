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

@transaction.atomic
def pay_travel_fee(order):
    wallet = Wallet.objects.select_for_update().get(user=order.customer)
    fee = quantize_amount(order.provider_service.travel_fee or 0)
    if fee <= 0:
        order.travel_fee_paid = True
        order.save()
        return
    if wallet.balance < fee:
        raise ValidationError("موجودی کیف پول کافی نیست")
    wallet.balance -= fee
    wallet.save()
    Transaction.objects.create(user=order.customer, order=order, transaction_type='payment', amount=fee,
                               description=f"هزینه ایاب و ذهاب {order.id}")
    order.travel_fee_paid = True
    order.save()

@transaction.atomic
def pay_service_fee_and_release(order, amount):
    amount = quantize_amount(amount)
    customer_wallet = Wallet.objects.select_for_update().get(user=order.customer)
    if customer_wallet.balance < amount:
        raise ValidationError("موجودی کیف پول کافی نیست")

    customer_wallet.balance -= amount
    customer_wallet.save()
    Transaction.objects.create(user=order.customer, order=order, transaction_type='payment', amount=amount,
                               description=f"Service fee paid for order {order.id}")

    # Commission & provider share
    commission_rate = get_commission_rate(order.provider)
    commission_amount = (amount * commission_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    provider_amount = (amount - commission_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    provider_wallet = Wallet.objects.select_for_update().get(user=order.provider.user)
    provider_wallet.balance += provider_amount
    provider_wallet.save()
    Transaction.objects.create(user=order.provider.user, order=order, transaction_type='payment', amount=provider_amount,
                               description=f"دریافتی ارائه دهنده {order.id}")

    Transaction.objects.create(user=None, order=order, transaction_type='commission', amount=commission_amount,
                               description=f"حق کمیسیون سفارش {order.id}")

