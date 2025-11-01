from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, unique=True)
    diagnostic = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.name