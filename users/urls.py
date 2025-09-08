from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register-provider/', RegisterProviderView.as_view(), name='register-provider'),
    path('verify-provider/<int:pk>/', verify_provider, name='verify-provider'),
]