from django.shortcuts import render
from django.db.models import Avg
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import User, Provider, Address
from .serializers import UserRegisterSerializer, ProviderRegisterSerializer, AddressSerializer
from rest_framework.decorators import api_view
from reviews.models import Review


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class RegisterProviderView(generics.CreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderRegisterSerializer


class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# @api_view(['POST'])
# def verify_provider(request, pk):
#     try:
#         p = Provider.objects.get(pk=pk)
#     except Provider.DoesNotExist:
#         return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
#     p.verified = True
#     p.save()
#     return Response({'detail': 'verified'})


class ProviderProfileView(generics.RetrieveAPIView):
    serializer_class = ProviderRegisterSerializer
    queryset = Provider.objects.all()

    def retrieve(self, request, *args, **kwargs):
        provider = self.get_object()
        avg_rating = Review.objects.filter(provider=provider).aggregate(Avg("rating"))["rating__avg"] or 0
        data = {
            "id": provider.id,
            "name": provider.user.username,
            "service": provider.main_category.name,
            "rating": round(avg_rating, 2)
        }
        return Response(data)