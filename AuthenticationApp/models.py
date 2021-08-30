from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# class User(AbstractUser):
    
#     class Meta:
#         pass

class Enterprises(models.Model):
    enterprise_id = models.IntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=100, null=False)
    tin = models.CharField(max_length=100, null=False)
    
    
    def __str__(self):
        return self.account_name