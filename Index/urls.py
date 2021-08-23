from django.urls import path 
from . import views
import Index


urlpatterns = [    
    path('', views.HomepageView.home_page, name='Homepage'),
    path('pricing', views.PricingView.pricing_page, name='Pricing')
    ]