from django.urls import path
from . import views


urlpatterns = [
    path('', views.DashboardView.main_dashboard, name='MainDashboard')
    ]