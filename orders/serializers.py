from rest_framework import serializers
from .models import Order, ProviderAvailability
from services.serializers import ProviderServiceSerializer
from users.serializers import AddressSerializer


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.username", read_only=True)
    provider_name = serializers.CharField(source="provider.user.username", read_only=True)
    provider_service_detail = ProviderServiceSerializer(source='provider_service', read_only=True)
    address_detail = AddressSerializer(source='address', read_only=True)

    class Meta:
        model = Order
        fields = ['id','customer','customer_username','provider','provider_username',
                  'provider_service','provider_service_detail','address','address_text',
                  'address_detail','scheduled_time','payment_method','status',
                  'travel_fee_paid','service_fee_paid','service_fee_amount','total_price',
                  'created_at','completed_at']
        read_only_fields = ['status','travel_fee_paid','service_fee_paid','total_price','created_at','completed_at']


class ProviderAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderAvailability
        fields = ['id', 'provider', 'start_time', 'end_time', 'is_booked']
        read_only_fields = ['is_booked', 'provider']