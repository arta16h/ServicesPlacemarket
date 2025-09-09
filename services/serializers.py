from rest_framework import serializers
from .models import ServiceCategory, SubCategory, ProviderService

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name", "category"]


class ProviderServiceSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source="subcategory.name", read_only=True)
    category_name = serializers.CharField(source="subcategory.category.name", read_only=True)

    class Meta:
        model = ProviderService
        fields = ["id", "subcategory", "subcategory_name", "category_name", "price", "base_fee"]
