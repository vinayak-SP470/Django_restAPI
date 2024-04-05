from django.contrib.auth.views import LoginView
from django.urls import path
from .views import seller_products, user_login, logout_user, user_signup, add_product, edit_product, delete_product

urlpatterns = [
    path('', seller_products, name='home'),
    path('seller_products/', seller_products, name='seller_products'),
    path('login', user_login, name='login'),
    path('logout', logout_user, name='logout'),
    path('signup', user_signup, name='signup'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
]
