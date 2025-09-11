import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .utils import get_commission_rate
from .serializers import WalletSerializer, TransactionSerializer
from orders.models import Order

# نمایش کیف پول
class WalletView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet

# نمایش تاریخچه معاملات
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by("-created_at")

# شارژ کیف پول 
class DepositWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = float(request.data.get("amount", 0))
        if amount <= 0:
            return Response({"error": "مقدار نامعتبر"}, status=status.HTTP_400_BAD_REQUEST)
        wallet = request.user.wallet
        wallet.balance += amount
        wallet.save()
        Transaction.objects.create(wallet=wallet, type="deposit", amount=amount)
        return Response({"message": "کیف پول شارژ شد", "اعتبار": wallet.balance})

# اتصال به زرین‌پال برای شارژ
class WalletDepositRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = int(request.data.get("amount", 0))
        if amount <= 0:
            return Response({"status": "failed", "reason": "amount must be > 0"}, status=400)

        req_data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": amount,
            "description": "شارژ کیف پول",
            "callback_url": settings.ZARINPAL_CALLBACK_URL,
        }
        response = requests.post(settings.ZARINPAL_REQUEST_URL, json=req_data).json()

        if response["data"]["code"] == 100:
            authority = response["data"]["authority"]
            payment_url = settings.ZARINPAL_STARTPAY_URL + authority
            return Response({"status": "ok", "url": payment_url})
        else:
            return Response({"status": "failed", "errors": response["errors"]}, status=400)

# برداشت از کیف پول (ویژه ارائه‌دهنده‌ها)
class WithdrawWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = float(request.data.get("amount", 0))
        wallet = request.user.wallet
        if amount <= 0 or amount > wallet.balance:
            return Response({"error": "مقدار نامعتبر"}, status=status.HTTP_400_BAD_REQUEST)
        wallet.balance -= amount
        wallet.save()
        Transaction.objects.create(wallet=wallet, type="withdraw", amount=amount)
        return Response({"message": "برداشت موفق", "balance": wallet.balance})

# پرداخت سفارش
class PayOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(id=pk, customer=request.user)
        except Order.DoesNotExist:
            return Response({"error": "سفارش موردنظر پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)

        if order.status != "accepted":
            return Response({"error": "بعد از تائید سفارش، میتوانید پرداخت کنید"}, status=status.HTTP_400_BAD_REQUEST)

        wallet = request.user.wallet
        if wallet.balance < order.total_price:
            return Response({"error": "موجودی ناکافی"}, status=status.HTTP_400_BAD_REQUEST)

        # کسر از کیف پول مشتری
        wallet.balance -= order.total_price
        wallet.save()
        Transaction.objects.create(wallet=wallet, order=order, type="payment", amount=order.total_price)

        # محاسبه کمیسیون
        commission_rate = get_commission_rate(provider=order.provider.user)
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

        return Response({"message": "پرداخت موفق", "comission": commission, "provider_amount": provider_amount})
    

