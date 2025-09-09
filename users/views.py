from django.shortcuts import render
from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, ProviderProfile
from .serializers import UserSerializer, ProviderProfileSerializer
from rest_framework.decorators import api_view
from reviews.models import Review


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


class ProviderProfileView(generics.RetrieveAPIView):
    serializer_class = ProviderProfileSerializer
    queryset = ProviderProfile.objects.all()

    def retrieve(self, request, *args, **kwargs):
        provider = self.get_object()
        avg_rating = Review.objects.filter(provider=provider).aggregate(Avg("rating"))["rating__avg"] or 0
        data = {
            "id": provider.id,
            "name": provider.user.username,
            "service": provider.service.name,
            "bio": provider.bio,
            "rating": round(avg_rating, 2)
        }
        return Response(data)