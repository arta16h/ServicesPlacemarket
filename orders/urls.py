from django.urls import path
from .views import (
    CreateOrderView, CustomerOrdersView, ProviderOrdersView,
    UpdateOrderStatusView, ProviderAvailabilityView, BookAvailabilityView, ProviderAvailabilityListView, 
)

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create-order"),
    path("my-orders/", CustomerOrdersView.as_view(), name="customer-orders"),
    path("provider-orders/", ProviderOrdersView.as_view(), name="provider-orders"),
    path("update-status/<int:pk>/", UpdateOrderStatusView.as_view(), name="update-order-status"),
    path("availability/create/", ProviderAvailabilityView.as_view(), name="create-availability"),
    path('availability/<int:pk>/book/', BookAvailabilityView.as_view(), name='book-availability'),
    path('availability/provider/<int:pk>/', ProviderAvailabilityListView.as_view(), name='provider-availability'),
]
