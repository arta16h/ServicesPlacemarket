from rest_framework import serializers
from .models import Wallet, Transaction
import logging
logger = logging.getLogger(__name__)


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "wallet", "order", "type", "amount", "created_at"]