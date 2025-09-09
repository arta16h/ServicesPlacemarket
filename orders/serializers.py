from rest_framework import serializers
from .models import Order, ProviderAvailability


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.username", read_only=True)
    provider_name = serializers.CharField(source="provider.user.username", read_only=True)
    service_name = serializers.CharField(source="service.subcategory.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "customer", "customer_name", "provider", "provider_name",
            "service", "service_name", "address", "datetime", "payment_method",
            "status", "total_price", "created_at"
        ]
        read_only_fields = ["status", "total_price"]


class ProviderAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderAvailability
        fields = ["id", "date", "start_time", "end_time"]