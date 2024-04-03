from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    empid = models.CharField(max_length=10, unique=True)
    designation = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    phonenumber = models.CharField(max_length=20, blank=False)
    email = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.name
