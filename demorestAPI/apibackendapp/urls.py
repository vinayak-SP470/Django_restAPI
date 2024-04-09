from django.urls import path
from .views import employee_list, set_session, get_session,create_checkout_session, send_otp, products, get_all_products, cartlist, delete_all_cartitems
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('send-otp/', send_otp, name='send_otp'),

    path('emp_list', employee_list),

    path('seller-product/', products, name='products'),
    path('all-products/', get_all_products, name='all_products'),
    path('cartitems/', cartlist, name='cartitems'),
    path('delete-all/cartitems/', delete_all_cartitems, name='delete_all_cartitems'),
    # path('payment/', payment_view, name='payment'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),

]





# path('set-session/', set_session, name='set_session'),
# path('get-session/', get_session, name='get_session'),