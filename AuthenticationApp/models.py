from django.db import models, utils
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.base_session import AbstractBaseSession
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
        
    @classmethod
    def add_new(self):
        enterprise_id = "OCECI-{0}".format(self.objects.count()+ 1)
        try:
            self.objects.create(
                enterprise_id = enterprise_id
                                )     
            return enterprise_id  

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
        try:
            if self.check_username(username=description['username']) == None:
                user_id = "OCAUTHUSR-{0}".format(self.objects.count()+ 1)
                self.objects.create(
                            id = user_id,
                            enterprise = Enterprises.objects.get(enterprise_id=description['enterprise_id']),
                            first_name = description['first_name'],
                            last_name = description['last_name'],
                            email = description['email'],
                            is_staff = description['is_staff'],
                            is_active = description['is_active'],
                            username = description['username'],
                            password = description['password'],
                            is_superuser = description['is_superuser'],
                            date_joined = datetime.now()
                            )
                return user_id
            else:
                return {'status':500, 'msg':'User Already Exist'}
        except utils.IntegrityError:
            return 500 
    
    @classmethod
    def check_username(self, username):
        try:
            return self.objects.get(username=username)
        except self.DoesNotExist:
            return None

    classmethod
    def check_email(self, email):
        try:
            return self.objects.get(email=email)
        except self.DoesNotExist:
            return None

    @classmethod
    def authenticate(self, request,username, password):
        try:
            return self.objects.get(username=username, password=password)
        except self.DoesNotExist:
            return None

    @property
    def hash(password, action):
        pass
