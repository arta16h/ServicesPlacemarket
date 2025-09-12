from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Provider, Address
from .utils import get_address_from_coords


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


class ProviderRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    phone_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Provider
        fields = ['id', 'username', 'password', 'email', 'phone_number', 'main_category', 'region', 'documents']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email', '')
        phone = validated_data.pop('phone_number', None)
        user = User.objects.create(username=username, email=email, role='provider', phone_number=phone)
        user.set_password(password)
        user.save()
        provider = Provider.objects.create(user=user, **validated_data)
        return provider
    

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'label', 'full_address', 'place_id', 'latitude', 'longitude', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        lat = validated_data.get("latitude")
        lng = validated_data.get("longitude")
        if lat and lng:
            validated_data["address"] = get_address_from_coords(lat, lng)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        lat = validated_data.get("latitude")
        lng = validated_data.get("longitude")
        if lat and lng:
            validated_data["address"] = get_address_from_coords(lat, lng)
        return super().update(instance, validated_data)