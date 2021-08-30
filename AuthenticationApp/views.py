from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login, authenticate, logout


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
                return redirect(resolve_url('Login'))
        else:
            return redirect(resolve_url('Login'))
        
    def logout(request):
        if request.method == "GET":
            logout(request)
            return redirect(resolve_url('Login'))
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
            print(request.POST.dict())
        return redirect(resolve_url('MainDashboard'))