from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Provider, Address
from services.serializers import ProviderServiceSerializer


User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone_number', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProviderProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ['id', 'user', 'main_category', 'service_area', 'document', 'verified']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_provider'] = True
        password = user_data.pop('password', None)
        user = User.objects.create(**user_data)
        if password:
            user.set_password(password)
            user.save()
        provider = Provider.objects.create(user=user, **validated_data)
        return provider
    

class ProviderProfileDetailSerializer(serializers.ModelSerializer):
    services = ProviderServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        fields = ["id", "main_category", "service_area", "document", "services"]