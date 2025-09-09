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

# برداشت از کیف پول (ویژه ارائه‌دهنده‌ها)
class WithdrawWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = float(request.data.get("amount", 0))
        wallet = request.user.wallet
        if amount <= 0 or amount > wallet.balance:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        wallet.balance -= amount
        wallet.save()
        Transaction.objects.create(wallet=wallet, type="withdraw", amount=amount)
        return Response({"message": "Withdrawal successful", "balance": wallet.balance})

# پرداخت سفارش
class PayOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(id=pk, customer=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status != "accepted":
            return Response({"error": "Order must be accepted before payment"}, status=status.HTTP_400_BAD_REQUEST)

        wallet = request.user.wallet
        if wallet.balance < order.total_price:
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        # کسر از کیف پول مشتری
        wallet.balance -= order.total_price
        wallet.save()
        Transaction.objects.create(wallet=wallet, order=order, type="payment", amount=order.total_price)

        # محاسبه کمیسیون
        commission_rate = 0.20  # 20%
        commission = order.total_price * commission_rate
        provider_amount = order.total_price - commission

        # واریز به کیف پول ارائه‌دهنده
        provider_wallet = order.provider.user.wallet
        provider_wallet.balance += provider_amount
        provider_wallet.save()
        Transaction.objects.create(wallet=provider_wallet, order=order, type="payment", amount=provider_amount)

        # ثبت کمیسیون
        Transaction.objects.create(wallet=wallet, order=order, type="commission", amount=commission)

        # تغییر وضعیت سفارش
        order.status = "done"
        order.save()

        return Response({"message": "Payment successful", "commission": commission, "provider_amount": provider_amount})