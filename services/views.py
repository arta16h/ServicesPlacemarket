from rest_framework import generics, filters, permissions, viewsets
from .models import ServiceCategory, SubCategory, ProviderService
from .serializers import ServiceCategorySerializer, SubCategorySerializer, ProviderServiceSerializer
import logging
logger = logging.getLogger(__name__)


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProviderServiceViewSet(viewsets.ModelViewSet):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'provider'):
            raise PermissionError("فقط ارائه دهندگان قادر به اضافه کردن سرویس هستند")
        serializer.save(provider=self.request.user.provider)


class SearchServiceView(generics.ListAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["subcategory__name", "subcategory__category__name", "provider__user__username"]
    ordering_fields = ["price"]
