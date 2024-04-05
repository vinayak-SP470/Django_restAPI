from django.shortcuts import render
from .serializers import EmployeeSerializer
from django.http import JsonResponse
from .models import Employee
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .decorators import validate_required_fields
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import random
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def hello_world(request):
    # request._logging_enabled = True
    return Response({'message': 'hai user'})


@swagger_auto_schema(
    method='post',
    operation_description="Add new employee",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'empid', 'designation', 'email'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Employee name'),
            'empid': openapi.Schema(type=openapi.TYPE_STRING, description='Employee ID'),
            'designation': openapi.Schema(type=openapi.TYPE_INTEGER, description='Employee designation ID'),
            'phonenumber': openapi.Schema(type=openapi.TYPE_STRING, description='Employee phone number', nullable=True),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Employee email'),
        }
    ),
    responses={201: openapi.Response("Employee added", EmployeeSerializer())}
)
@swagger_auto_schema(
    method='delete',
    operation_description="Delete an employee by ID",
    manual_parameters=[
        openapi.Parameter(
            name='id',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='ID of the employee to delete',
            required=True,
        ),
    ],
    responses={
        status.HTTP_204_NO_CONTENT: 'Employee deleted successfully',
        status.HTTP_400_BAD_REQUEST: 'Bad request (e.g., missing ID)',
        status.HTTP_404_NOT_FOUND: 'Employee not found',
    }
)

# Inbuilt decorator use
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
@validate_required_fields(['name', 'empid', 'designation', 'email'])
@permission_classes([IsAuthenticated])

def employee_list(request):
    if request.method == 'GET':
        employee_list = Employee.objects.all()
        employee_list_serializer = EmployeeSerializer(employee_list, many=True)
        return JsonResponse(employee_list_serializer.data, safe=False)
    elif request.method == 'POST':
        employee_add_serializer = EmployeeSerializer(data=request.data)
        if employee_add_serializer.is_valid():
            employee_add_serializer.save()
            return JsonResponse(employee_add_serializer.data, status=201)
        return JsonResponse(employee_add_serializer.errors, status=400)
    elif request.method == 'PUT':
        try:
            employee_instance = Employee.objects.get(id=request.data.get('id'))
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)

        employee_update_serializer = EmployeeSerializer(employee_instance, data=request.data)
        if employee_update_serializer.is_valid():
            employee_update_serializer.save()
            return JsonResponse(employee_update_serializer.data)
        return JsonResponse(employee_update_serializer.errors, status=400)
    elif request.method == 'DELETE':
        employee_id = request.query_params.get('id')
        if not employee_id:
            return JsonResponse({'error': 'Employee ID is required'}, status=400)

        try:
            employee_instance = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)

        deleted_employee_id = employee_instance.id
        employee_instance.delete()

        response_data = {
            'message': f'Employee with ID {deleted_employee_id} deleted successfully',
            'deleted_employee_id': deleted_employee_id
        }
        return JsonResponse(response_data, status=204)



# Example of using default milldleware(SessionMiddleware)
def set_session(request):
    request.session['user_id'] = 123
    return HttpResponse("Session value set")

def get_session(request):
    user_id = request.session.get('user_id')
    if user_id:
        return HttpResponse(f"User ID from session: {user_id}")
    else:
        return HttpResponse("User ID not found in session")

# function to send otp message
def send_otp(request):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    account_sid = 'AC280b3c09f52e459c313696edd0fdd7d9'
    auth_token = 'ce944f4fa0d3b0a35118c773e628d9ef'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_='+13346030803',
        to='+918129110726'
    )
    return JsonResponse({'message': 'OTP sent successfully', 'otp': otp, 'message_sid': message.sid})

