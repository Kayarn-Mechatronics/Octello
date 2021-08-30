from django.contrib.auth import logout
from django.urls import path 
from . import views


urlpatterns = [    
    path('', views.AuthenticationApi.authenticate, name='Authenticate'),

    #Login View & Logout Request Path
    path('login', views.LoginView.login_page, name='Login_Page'),
    path('logout', views.AuthenticationApi.logout, name='LogoutRequest'),

    #Registration View
    path('register', views.RegisterView.register_page, name='Registration_Page'),
    path('enroll', views.RegisterView.register, name='Enroll')
    ]