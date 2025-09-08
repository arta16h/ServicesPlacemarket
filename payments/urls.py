from django.urls import path
from .views import WalletDetailView, TransactionListCreateView


urlpatterns = [
    path('wallet/<int:pk>/', WalletDetailView.as_view(), name='wallet-detail'),
    path('transactions/', TransactionListCreateView.as_view(), name='transactions'),
]