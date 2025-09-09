from django.urls import path
from .views import WalletView, DepositWalletView, WithdrawWalletView, PayOrderView

urlpatterns = [
    path("wallet/", WalletView.as_view(), name="wallet"),
    path("deposit/", DepositWalletView.as_view(), name="deposit-wallet"),
    path("withdraw/", WithdrawWalletView.as_view(), name="withdraw-wallet"),
    path("pay/<int:pk>/", PayOrderView.as_view(), name="pay-order"),
]
