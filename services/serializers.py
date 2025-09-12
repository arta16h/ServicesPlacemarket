from rest_framework import serializers
from .models import ServiceCategory, SubCategory, ProviderService
import logging
logger = logging.getLogger(__name__)


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name", "category"]


class ProviderServiceSerializer(serializers.ModelSerializer):
    provider_username = serializers.CharField(source='provider.user.username', read_only=True)
    
    class Meta:
        model = ProviderService
        fields = ['id', 'provider', 'provider_username', 'subcategory', 'price', 'travel_fee', 'description']
        read_only_fields = ['provider']
