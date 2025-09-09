from django.urls import path
from .views import (
    ServiceCategoryListView,
    SubCategoryListView,
    ProviderServiceListCreateView,
    SearchServiceView
)

urlpatterns = [
    path("categories/", ServiceCategoryListView.as_view(), name="categories"),
    path("subcategories/", SubCategoryListView.as_view(), name="subcategories"),
    path("my-services/", ProviderServiceListCreateView.as_view(), name="my-services"),
    path("search/", SearchServiceView.as_view(), name="search-services"),
]
