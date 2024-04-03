from django.shortcuts import render
from .serializers import EmployeeSerializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .models import Employee
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, World!'})


@swagger_auto_schema(
    method='post',
    operation_description="Add new employee",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'empid', 'designation', 'phonenumber', 'email'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Employee name'),
            'empid': openapi.Schema(type=openapi.TYPE_STRING, description='Employee ID'),
            'designation': openapi.Schema(type=openapi.TYPE_INTEGER, description='Employee designation ID'),
            'phonenumber': openapi.Schema(type=openapi.TYPE_STRING, description='Employee phone number'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Employee email'),
        }
    ),
    responses={201: openapi.Response("Employee added", EmployeeSerializer())}
)
@api_view(['GET', 'POST'])
def employee_list(request):
    if request.method == 'GET':
        employee_list = Employee.objects.all()
        employee_list_serializer = EmployeeSerializer(employee_list, many=True)
        return JsonResponse(employee_list_serializer.data, safe=False)
    elif request.method =='POST':
        request_data = JSONParser().parse(request)
        employee_add_serializer = EmployeeSerializer(data = request_data)
        if employee_add_serializer.is_valid():
            employee_add_serializer.save()
            return JsonResponse(employee_add_serializer.data, status=201)
        return JsonResponse(employee_add_serializer.errors, status= 400)
