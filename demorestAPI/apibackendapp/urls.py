from django.urls import path
from .views import employee_list, hello_world, my_view, set_session, get_session

urlpatterns = [
    path('emp_list', employee_list),
    path('hello/', hello_world, name='hello-world'),
    path('',my_view),
    path('set-session/', set_session, name='set_session'),
    path('get-session/', get_session, name='get_session'),
    ]