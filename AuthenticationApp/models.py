from django.db import models
from django.contrib.auth.models import AbstractUser
from django import utils
from datetime import *

class Enterprises(models.Model):
    enterprise_id = models.CharField(primary_key=True, max_length=20, null=False, unique=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    tin = models.CharField(max_length=100, null=True)
    plan = models.CharField(max_length=100, null=True)
    configurations = models.JSONField(max_length=100, null=True)
   
    def __str__(self):
        return self.account_name
    
    def enroll(self, description):
        enterprise_id = "OCECI-{0}".format(self.objects.count()+ 1)
        try:
            self.objects.create(
                enterprise_id = enterprise_id,
                name = description['name']  
                                )        

        except utils.IntegrityError:
            return False
    
class User(AbstractUser):
    id = models.CharField(primary_key=True, max_length=20, null=False, unique=True)
    enterprise = models.ForeignKey(Enterprises, on_delete=models.CASCADE)
    permissions = models.JSONField(null=True)     
    
    class Meta:
        pass
     
    @classmethod 
    def add_user(self, description):
        user_id = "OCAUTHUSR-{0}".format(self.objects.count()+ 1)
        self.objects.create(
                            id = user_id,
                            enterprise = Enterprises.objects.get(description['enterprise_id']),
                            first_name = description['first_name'],
                            last_name = description['last_name'],
                            email = description['email'],
                            is_staff = description['is_staff'],
                            is_admin = description['is_admin'],
                            is_active = description['is_active'],
                            username = description['username'],
                            password = description['password'],
                            is_superuser = description['is_superuser'],
                            date_joined = datetime.now()
                            )
    
    def hash(password):
        pass
    
    