from django.urls import path
from .views import (WalletView, DepositWalletView, WithdrawWalletView, 
        PayOrderView, TransactionListView, WalletDepositRequestView, WalletDepositCallbackView)

urlpatterns = [
    path("wallet/", WalletView.as_view(), name="wallet"),
    path("wallet/deposit/request/", WalletDepositRequestView.as_view(), name="wallet-deposit-request"),
    path("callback/", WalletDepositCallbackView.as_view(), name="wallet_callback"),
    path("transactions/", TransactionListView.as_view(), name="transactions"),
    path("deposit/", DepositWalletView.as_view(), name="deposit-wallet"),
    path("withdraw/", WithdrawWalletView.as_view(), name="withdraw-wallet"),
    path("pay/<int:pk>/", PayOrderView.as_view(), name="pay-order"),
]
