from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone', 'user_image', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data.get('email'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Неверный email или пароль")
        if not user.is_active:
            raise serializers.ValidationError("Пользователь не активен")
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'user_image', 'phone']

class CourierSerializer (serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuCategorySerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = MenuCategory
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    category = MenuCategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    courier = CourierSerializer(read_only=True)
    items = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'courier', 'total_price', 'status', 'created_at', 'items']


class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    courier = CourierSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
