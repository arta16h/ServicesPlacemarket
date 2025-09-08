from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, ProviderProfile
from .serializers import UserSerializer, ProviderProfileSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
