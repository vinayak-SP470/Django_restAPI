from django.urls import path
from .views import employee_list, hello_world

urlpatterns = [
    path('emp_list', employee_list),
    path('hello/', hello_world, name='hello-world'),
    ]