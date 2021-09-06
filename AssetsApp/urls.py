from django.urls import path
from . import views

urlpatterns = [
    #Assets Section
    path('all', views.AssetsView.all_assets, name='AssetsList'),
    path('lookup', views.AssetsView.lookup, name='Lookup_Asset'),
    path('add', views.AssetsView.add_asset, name='Add_Asset'),
    path('<str:asset_id>/statement', views.AssetsView.statement, name='Asset_Statement'),
    
    #Categories
    path('categories/add_category', views.AssetsView.add_category, name='Add_Assets_Category'),
    path('categories/add_subcategory', views.AssetsView.add_category, name='Add_Assets_SubCategory'),
    
    #Transactions
    path('transactions', views.TransactionView.all_transactions, name='Assets_Transactions')
    ]