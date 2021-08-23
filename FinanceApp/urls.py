from FinanceApp.models import Accounts
from django.urls import path
from . import views

urlpatterns = [
    #Accounts Section
    path('accounts', views.AccountsView.all_accounts, name='Accounts'),
    path('accounts/lookup', views.AccountsView.lookup, name='Lookup_Account'),
    path('accounts/add_account', views.AccountsView.add_account, name='Add_Account'),
    path('account/<str:account_id>/statement', views.AccountsView.statement, name='Account_Statement'),
    
    #Categories
    path('categories', views.CategoriesView.all_categories, name='Transaction_Categories'),
    
    #Transactions
    path('transactions', views.TransactionView.all_transactions, name='Transactions')
    ]