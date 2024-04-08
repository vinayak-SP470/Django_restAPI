from rest_framework import serializers
from .models import Role1, Employee
from AppEcommerce.models import Product, CartItem

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role1
        fields ='__all__'

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