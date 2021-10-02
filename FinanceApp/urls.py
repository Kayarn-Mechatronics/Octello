from FinanceApp.models import Accounts
from django.urls import path
from . import views

urlpatterns = [
    #Accounts Section
    path('accounts', views.AccountsView.all_accounts, name='Accounts'),
    path('accounts/lookup', views.AccountsView.lookup, name='Lookup_Account'),
    path('accounts/addt', views.AccountsView.add_account, name='Add_Account'),
    path('accounts/categories', views.AccountsView.categories, name='Account_Categories'),
    path('accounts/categories/add', views.AccountsView.add_category, name='Add_Account_Category'),
    path('account/<str:account_id>/statement', views.AccountsView.statement, name='Account_Statement'),
    
    #Transactions
    path('transactions', views.TransactionView.all_transactions, name='Transactions'),
    path('transactions/add', views.TransactionView.add_transaction, name='Add_Transaction'),
    path('transactions/categories', views.TransactionView.add_transaction, name='Transaction_Categories'),
    path('transactions/categories/add', views.TransactionView.add_category, name='FinanceApp/Add_Transaction_Category'),
    path('transactions/subcategories', views.TransactionView.add_transaction, name='FinanceApp/Transaction_SubCategories'),
    path('transactions/subcategories/add', views.TransactionView.add_sub_category, name='FinanceApp/Add_Transaction_SubCategory')
    ]