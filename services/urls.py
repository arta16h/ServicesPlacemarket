# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceCategoryViewSet,
    SubCategoryViewSet,
    ProviderServiceViewSet,
    SearchServiceView,
)
import logging
logger = logging.getLogger(__name__)


# router برای ویوست‌ها
router = DefaultRouter()
router.register(r'service-categories', ServiceCategoryViewSet, basename='service-category')
router.register(r'subcategories', SubCategoryViewSet, basename='subcategory')
router.register(r'provider-services', ProviderServiceViewSet, basename='provider-service')

urlpatterns = [
    path('search-services/', SearchServiceView.as_view(), name='search-services'),
    path('', include(router.urls)),
]
