from django.contrib import admin
from .models import Role, CustomUser, Product, Cart , CartItem

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)