from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import WalletSerializer, TransactionSerializer
from orders.models import Order

# نمایش کیف پول
class WalletView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet

# شارژ کیف پول 
class DepositWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = float(request.data.get("amount", 0))
        if amount <= 0:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        wallet = request.user.wallet
        wallet.balance += amount
        wallet.save()
        Transaction.objects.create(wallet=wallet, type="deposit", amount=amount)
        return Response({"message": "Wallet charged", "balance": wallet.balance})

