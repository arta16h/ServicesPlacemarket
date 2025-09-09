from django.urls import path
from .views import WalletView, DepositWalletView, WithdrawWalletView, PayOrderView, TransactionListView

urlpatterns = [
    path("wallet/", WalletView.as_view(), name="wallet"),
    path("transactions/", TransactionListView.as_view(), name="transactions"),
    path("deposit/", DepositWalletView.as_view(), name="deposit-wallet"),
    path("withdraw/", WithdrawWalletView.as_view(), name="withdraw-wallet"),
    path("pay/<int:pk>/", PayOrderView.as_view(), name="pay-order"),
]
