from django.contrib import admin
from .models import Role, Employee, APILog
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(APILog)