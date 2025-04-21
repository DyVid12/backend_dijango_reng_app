from rest_framework import serializers
from .models import CustomUser  # Import the correct model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Use your custom user model
        fields = ['id', 'username', 'email', 'gender'] 


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
