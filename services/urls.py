from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceCategoryViewSet, SubCategoryViewSet, ProviderServiceViewSet


router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'provider-services', ProviderServiceViewSet)


urlpatterns = [
    path('', include(router.urls)),
]