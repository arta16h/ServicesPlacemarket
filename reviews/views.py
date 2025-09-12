from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer
from users.models import ProviderProfile
from orders.models import Order
from django.db.models import Avg, Count
import logging
logger = logging.getLogger(__name__)

# ثبت نظر و امتیاز
class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order_id = self.request.data.get("order")
        try:
            order = Order.objects.get(id=order_id, customer=self.request.user, status="done")
        except Order.DoesNotExist:
            raise ValueError("Invalid order or not completed")

        if hasattr(order, "review"):
            raise ValueError("This order already has a review")

        serializer.save(
            customer=self.request.user,
            provider=order.provider,
            order=order
        )

# نمایش نظرات ارائه‌دهنده
class ProviderReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        provider_id = self.kwargs["pk"]
        return Review.objects.filter(provider_id=provider_id)

# لیدربرد بر اساس امتیاز
class LeaderboardView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        providers = ProviderProfile.objects.annotate(
            avg_rating=Avg("reviews__rating"),
            total_reviews=Count("reviews")
        ).order_by("-avg_rating", "-total_reviews")[:10]

        data = [
            {
                "provider": p.user.username,
                "service": p.service.name,
                "avg_rating": p.avg_rating or 0,
                "total_reviews": p.total_reviews
            }
            for p in providers
        ]
        return Response(data)
