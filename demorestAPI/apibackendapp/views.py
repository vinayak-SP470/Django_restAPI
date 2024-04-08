from django.shortcuts import render

from .renderers import CustomJSONRenderer, ProductJSONRenderer
from .serializers import EmployeeSerializer, ProductSerializer, CartItemSerializer
from django.http import JsonResponse
from .models import Employee
from rest_framework.decorators import api_view, permission_classes, renderer_classes
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
from rest_framework.response import Response
from AppEcommerce.models import Role, Product, Cart, CartItem
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login



# from ..AppEcommerce.models import Product


# @api_view(['GET'])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def hello_world(request):
#     # request._logging_enabled = True
#     return Response({'message': 'hai user'})

#
# @swagger_auto_schema(
#     method='post',
#     operation_description="Add new employee",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=['name', 'empid', 'designation', 'email'],
#         properties={
#             'name': openapi.Schema(type=openapi.TYPE_STRING, description='Employee name'),
#             'empid': openapi.Schema(type=openapi.TYPE_STRING, description='Employee ID'),
#             'designation': openapi.Schema(type=openapi.TYPE_INTEGER, description='Employee designation ID'),
#             'phonenumber': openapi.Schema(type=openapi.TYPE_STRING, description='Employee phone number', nullable=True),
#             'email': openapi.Schema(type=openapi.TYPE_STRING, description='Employee email'),
#         }
#     ),
#     responses={201: openapi.Response("Employee added", EmployeeSerializer())}
# )
# @swagger_auto_schema(
#     method='delete',
#     operation_description="Delete an employee by ID",
#     manual_parameters=[
#         openapi.Parameter(
#             name='id',
#             in_=openapi.IN_QUERY,
#             type=openapi.TYPE_INTEGER,
#             description='ID of the employee to delete',
#             required=True,
#         ),
#     ],
#     responses={
#         status.HTTP_204_NO_CONTENT: 'Employee deleted successfully',
#         status.HTTP_400_BAD_REQUEST: 'Bad request (e.g., missing ID)',
#         status.HTTP_404_NOT_FOUND: 'Employee not found',
#     }
# )

# Inbuilt decorator use
@csrf_exempt
# @api_view(['GET', 'POST', 'DELETE'])
@validate_required_fields(['name', 'empid', 'designation', 'email'])
# @permission_classes([IsAuthenticated])
@renderer_classes([CustomJSONRenderer])
def employee_list(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            employee_list = Employee.objects.all()
            employee_list_serializer = EmployeeSerializer(employee_list, many=True)
            return Response({'data': employee_list_serializer.data}, status=status.HTTP_200_OK)
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
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_='+13346030803',
        to='+918129110726'
    )
    return JsonResponse({'message': 'OTP sent successfully', 'otp': otp, 'message_sid': message.sid})


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('searchproduct', openapi.IN_QUERY, description="Search term for products",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('sort_by', openapi.IN_QUERY, description="Field to sort by", type=openapi.TYPE_STRING),
        openapi.Parameter('ascending', openapi.IN_QUERY, description="Sort order (asc or desc)",
                          type=openapi.TYPE_BOOLEAN),
    ]
)
@swagger_auto_schema(
    method='post',
    operation_description="Add a new product",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['productname', 'description', 'price', 'image'],
        properties={
            'productname': openapi.Schema(type=openapi.TYPE_STRING, description='Product name'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Product description'),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Product price'),
        }
    ),
    responses={
        201: openapi.Response("Product added", ProductSerializer()),
        400: "Bad Request: Invalid input data",
        401: "Unauthorized: Authentication credentials were not provided",
    }
)

@swagger_auto_schema(
    method='patch',
    operation_description="Update a product by ID",
    manual_parameters=[
        openapi.Parameter(
            name='product_id',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='ID of the product to update',
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'productname': openapi.Schema(type=openapi.TYPE_STRING, description='Product name', nullable=True),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Product description', nullable=True),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Product price', nullable=True),
        }
    ),
    responses={
        status.HTTP_200_OK: 'Product updated successfully',
        status.HTTP_400_BAD_REQUEST: 'Bad request (e.g., missing ID or invalid data)',
        status.HTTP_403_FORBIDDEN: 'Unauthorized to update this product',
        status.HTTP_404_NOT_FOUND: 'Product not found',
    }
)
@swagger_auto_schema(
    method='delete',
    operation_description="Delete a product by ID",
    manual_parameters=[
        openapi.Parameter(
            name='product_id',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='ID of the product to delete',
            required=True,
        ),
    ],
    responses={
        status.HTTP_204_NO_CONTENT: 'Product deleted successfully',
        status.HTTP_400_BAD_REQUEST: 'Bad request (e.g., missing ID)',
        status.HTTP_403_FORBIDDEN: 'Unauthorized to delete this product',
        status.HTTP_404_NOT_FOUND: 'Product not found',
    }
)
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@renderer_classes([ProductJSONRenderer])

def products(request):
    if not request.user.is_authenticated or request.user.role.name != 'Seller':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        searchterm = request.GET.get('searchproduct')
        sort_by = request.GET.get('sort_by', 'price')
        ascending = request.GET.get('ascending', 'true').lower() == 'true'

        if searchterm:
            products = Product.objects.filter(productname__icontains=searchterm)
        else:
            products = Product.objects.filter(seller=request.user)

        if sort_by == 'price':
            if ascending:
                products = products.order_by('price')
            else:
                products = products.order_by('-price')

        serializer = ProductSerializer(products, many=True)
        return  Response({'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        product_id = request.query_params.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            # Check if the product belongs to the current user
            if product.seller != request.user:
                return Response({'error': 'Unauthorized to update this product'}, status=status.HTTP_403_FORBIDDEN)

            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        product_id = request.query_params.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            # Check if the product belongs to the current user
            if product.seller != request.user:
                return Response({'error': 'Unauthorized to delete this product'}, status=status.HTTP_403_FORBIDDEN)
            product.delete()
            return Response({'success': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_all_products(request):
    if not request.user.is_authenticated or request.user.role.name != 'Customer':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



@api_view(['GET'])
def cartlist(request):
    if not request.user.is_authenticated or request.user.role.name != 'Customer':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        try:
            customer_cart = Cart.objects.get(customer=request.user)
            cart_items = CartItem.objects.filter(cart=customer_cart)
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)








# class CustomAuthenticationForm(AuthenticationForm):
#     error_messages = {
#         'invalid_login': "Please enter a correct username and password. Both fields may be case-sensitive.",
#     }
# @api_view(['POST'])
# def user_login(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, data=request.data)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     else:
#         return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)