from django.shortcuts import render
from rest_framework import generics
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
