from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, ProviderAvailability
from .serializers import OrderSerializer, ProviderAvailabilitySerializer
from services.models import ProviderService

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


