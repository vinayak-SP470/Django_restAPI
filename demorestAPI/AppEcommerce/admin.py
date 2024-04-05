from django.contrib import admin

# Register your models here.
from .models import Role, CustomUser, Product
admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Product)
