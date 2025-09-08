from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, ProviderProfile
from .serializers import UserSerializer, ProviderProfileSerializer
from rest_framework.decorators import api_view

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterProviderView(generics.CreateAPIView):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer


@api_view(['POST'])
def verify_provider(request, pk):
    try:
        p = ProviderProfile.objects.get(pk=pk)
    except ProviderProfile.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    p.verified = True
    p.save()
    return Response({'detail': 'verified'})