from rest_framework import generics, filters
from .models import ServiceCategory, SubCategory, ProviderService
from .serializers import ServiceCategorySerializer, SubCategorySerializer, ProviderServiceSerializer
from rest_framework.permissions import IsAuthenticated


class ServiceCategoryListView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class SubCategoryListView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ProviderServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ProviderServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProviderService.objects.filter(provider__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user.providerprofile)


class SearchServiceView(generics.ListAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["subcategory__name", "subcategory__category__name", "provider__user__username"]
    ordering_fields = ["price"]
