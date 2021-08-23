from django.urls import path
from . import views

urlpatterns = [
    path('list', views.WizzardsListView.wizzards_list, name='WizzardsList')
    ]