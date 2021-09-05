from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login, authenticate, logout
from . import models


# Create your views here.
class AuthenticationApi:
    def authenticate(request):
        if request.method == "POST":
            credentials = request.POST.dict()
            user = authenticate(request, username=credentials['username'], password=credentials['password'])
            if user:
                login(request, user)
                return redirect(resolve_url('MainDashboard'))
            else:
                return redirect(resolve_url('Login_Page'))
        else:
            return redirect(resolve_url('Login_Page'))
        
    def logout(request):
        if request.method == "GET":
            logout(request)
            return redirect(resolve_url('Login_Page'))
        else:
            return redirect(resolve_url('MainDashboard'))
            
            
            
class LoginView:
    def login_page(request):
        return render(request, 'AuthenticationApp/Login.html')
    
class RegisterView:
    def register_page(request):
        return render(request, 'AuthenticationApp/Register.html')

    def register(request):
        if request.method == "POST":
            description = request.POST.dict()
            description['username'] = description['email']
            description['enterprise_id'] = models.Enterprises.add_new()
            description['is_staff'] = 1
            description['is_admin'] = 1
            description['is_active'] = 1
            description['is_superuser'] = 0
            if description['password'] != description['password_re']:
                print('Password do not match')
                return redirect(resolve_url('Registration_Page'))
            else:
                print(models.User.add_user(description))
                return redirect(resolve_url('Registration_Page'))
        else:
            return redirect(resolve_url('Registration_Page'))