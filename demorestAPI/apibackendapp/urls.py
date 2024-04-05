from django.urls import path
from .views import employee_list, hello_world, set_session, get_session, send_otp
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('emp_list', employee_list),
    path('hello/', hello_world, name='hello-world'),
    path('set-session/', set_session, name='set_session'),
    path('get-session/', get_session, name='get_session'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-otp/', send_otp, name='send_otp'),

]