from rest_framework import serializers
from .models import Review
import logging
logger = logging.getLogger(__name__)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "order", "customer", "provider", "rating", "comment", "created_at"]
        read_only_fields = ["customer", "provider", "created_at"]