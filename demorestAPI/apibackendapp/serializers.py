from rest_framework import serializers
from .models import Role, Employee

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields ='__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields ='__all__'