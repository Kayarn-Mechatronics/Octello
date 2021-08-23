from django.contrib.auth import logout
from django.urls import path 
from . import views


urlpatterns = [    
    path('login', views.LoginView.login_page, name='Login'),
    path('', views.AuthenticationApi.authenticate, name='Authenticate'),
    path('logout', views.AuthenticationApi.logout, name='LogoutRequest')
    ]