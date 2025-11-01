from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Kinesiologist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, unique=True)
    specialty = models.CharField(max_length=100)
    email = models.EmailField(max_length=60)
    phone_number = models.CharField(max_length=10)
    box = models.CharField(max_length=10)
    image_url = models.CharField(max_length=100)

    def __str__(self):
        return self.name