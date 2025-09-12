from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, ProviderAvailability
from payments.models import Wallet, Transaction
from .serializers import OrderSerializer, ProviderAvailabilitySerializer
from services.models import ProviderService
from payments.utils import pay_travel_fee, get_commission_rate
import datetime
import logging
logger = logging.getLogger(__name__)

# مشتری سفارش ایجاد می‌کند
class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        service = ProviderService.objects.get(id=self.request.data["service"])
        total_price = service.price + service.base_fee
        serializer.save(customer=self.request.user, provider=service.provider, total_price=total_price)

# لیست سفارش‌های مشتری
class CustomerOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

# لیست سفارش‌های ارائه‌دهنده
class ProviderOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(provider__user=self.request.user)

# ارائه‌دهنده سفارش را تایید یا رد می‌کند
class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(id=pk, provider__user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        if new_status not in ["accepted", "rejected", "done", "canceled"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)

# مدیریت تقویم کاری ارائه‌دهنده
class ProviderAvailabilityView(generics.ListCreateAPIView):
    serializer_class = ProviderAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProviderAvailability.objects.filter(provider__user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role != "provider":
            raise PermissionError("Only providers can add availability")
        serializer.save(provider=self.request.user.provider)

# لیست تایم‌های آزاد یک ارائه‌دهنده
class ProviderAvailabilityListView(generics.ListAPIView):
    serializer_class = ProviderAvailabilitySerializer

    def get_queryset(self):
        provider_id = self.kwargs["pk"]
        return ProviderAvailability.objects.filter(provider_id=provider_id, is_booked=False, start_time__gte=datetime.now())

# رزرو تایم توسط مشتری
class BookAvailabilityView(generics.UpdateAPIView):
    serializer_class = ProviderAvailabilitySerializer
    queryset = ProviderAvailability.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        availability = self.get_object()
        if availability.is_booked:
            raise PermissionError("این تایم قبلا رزرو شده است")
        service_id = self.request.data.get('provider_service')
        if not service_id:
            raise PermissionError("provider_service field required")
        provider_service = get_object_or_404(ProviderService, id=service_id)

        if provider_service.provider != availability.provider:
            raise PermissionError("خدمات انتخاب شده با ارئه دهنده مغایرت دارد")
        # create order
        order = Order.objects.create(
            customer=self.request.user,
            provider=availability.provider,
            provider_service=provider_service,
            address=self.request.user.addresses.first(),
            address_text=(self.request.data.get('address_text') or None),
            scheduled_time=availability.start_time,
            payment_method=self.request.data.get('payment_method', 'wallet'),
            total_price = provider_service.price + provider_service.travel_fee
        )
        availability.is_booked = True
        availability.save()

        if order.payment_method == 'wallet' and provider_service.travel_fee and provider_service.travel_fee > 0:
            pay_travel_fee(order)
        serializer.save(is_booked=True)

def complete_order(order):
    customer_wallet = order.customer.wallet
    provider_wallet = order.provider.user.wallet

    amount = order.service_price  # مبلغ سفارش
    commission_rate = get_commission_rate(order.provider)  # کمیسیون پویا
    commission_amount = amount * commission_rate
    provider_amount = amount - commission_amount

    # انتقال مبلغ
    provider_wallet.balance += provider_amount
    provider_wallet.save()

    # ثبت تراکنش برای ارائه‌دهنده
    Transaction.objects.create(
        user=order.provider.user,
        transaction_type="payment",
        amount=provider_amount,
        description=f"Order {order.id} payment after commission"
    )

    # ثبت تراکنش کمیسیون
    Transaction.objects.create(
        user=None,
        transaction_type="commission",
        amount=commission_amount,
        description=f"Commission from order {order.id}"
    )

    order.status = "done"
    order.save()
