from django.urls import path
from .views import (
    CreateOrderView, CustomerOrdersView, ProviderOrdersView,
    UpdateOrderStatusView, ProviderAvailabilityView
)

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create-order"),
    path("my-orders/", CustomerOrdersView.as_view(), name="customer-orders"),
    path("provider-orders/", ProviderOrdersView.as_view(), name="provider-orders"),
    path("update-status/<int:pk>/", UpdateOrderStatusView.as_view(), name="update-order-status"),
    path("availability/", ProviderAvailabilityView.as_view(), name="provider-availability"),
]
