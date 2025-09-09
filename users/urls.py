from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register-provider/', RegisterProviderView.as_view(), name='register-provider'),
    path('addresses/', AddressListCreateView.as_view(), name='addresses'),
    path('provider-profile/', ProviderProfileView.as_view(), name='provider-profile'),
]