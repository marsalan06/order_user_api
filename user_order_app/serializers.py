from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}
    is_superuser = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            is_superuser=validated_data.get('is_superuser', False)
        )
        return user




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'item', 'created_at')
        read_only_fields = ('id', 'created_at')