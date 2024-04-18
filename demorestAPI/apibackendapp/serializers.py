from rest_framework import serializers
from .models import Role1, Employee
from AppEcommerce.models import Product, CartItem, CustomUser, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role1
        fields ='__all__'

class RoleSerializerEcommerce(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields ='__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'productname', 'description', 'price')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['seller'] = user
        return super().create(validated_data)

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields ='__all__'