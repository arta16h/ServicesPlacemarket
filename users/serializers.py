from rest_framework import serializers
from .models import User, ProviderProfile




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password', 'is_customer', 'is_provider', 'default_address']


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user




class ProviderProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()


    class Meta:
        model = ProviderProfile
        fields = ['id', 'user', 'main_category', 'service_area', 'document', 'verified']


    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_provider'] = True
        password = user_data.pop('password', None)
        user = User.objects.create(**user_data)
        if password:
            user.set_password(password)
            user.save()
        provider = ProviderProfile.objects.create(user=user, **validated_data)
        return provider