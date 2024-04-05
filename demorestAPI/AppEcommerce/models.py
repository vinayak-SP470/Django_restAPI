from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager



class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=20, blank=False)


class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    productname = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.productname