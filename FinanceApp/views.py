from django.core.serializers import serialize
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from . import models
from datetime import *

# Create your views here.
class AccountsView:
    def all_accounts(request):
        context = {'Accounts' : models.Accounts.objects.filter(enterprise_id=request.user.enterprise_id)}
        context['AccountFormContext'] = {'Categories' : models.AccountsCategories.objects.filter(enterprise_id=request.user.enterprise_id)}
        return render(request, 'FinanceApp/Accounts/Accounts.html', context)
    
    def add_account(request):
        if request.method == 'POST':
            enterprise = request.user.enterprise_id
            user= request.user.id
            description = request.POST.dict()
            account_id = models.Accounts.add_account(enterprise, user, description)
            if account_id != False:
                if int(request.POST.dict()['balance']) != 0:
                    models.Accounts.starting_balance(account_id, int(request.POST.dict()['balance_flow']),int(request.POST.dict()['balance']), request.POST.dict()['currency'])
                    return redirect(resolve_url('Accounts'))
                else:
                    return redirect(resolve_url('Accounts'))
            else:
                return redirect(resolve_url('Accounts'))
        else:
            return redirect(resolve_url('Accounts'))

    def add_category(request):
        if request.method == 'POST':
            enterprise = request.user.enterprise_id
            user= request.user.id
            description = request.POST.dict()
            models.AccountsCategories.add_category(enterprise, user, description)
            return redirect(resolve_url('Accounts'))
        else:
            return redirect(resolve_url('Accounts'))

    def categories(request):
        pass

    def lookup(request):
        if request.method == 'GET':
            print(dir(request.body))
            return HttpResponse(True)
        
        
    def statement(request, account_id):
        print(account_id)
        return render(request, 'FinanceApp/Accounts/statements.html')  
    
     
class TransactionView:
    def all_transactions(request):
        print(models.TransactionsDB.to_json())
        context= models.TransactionsDB.to_json()
        return render(request, 'FinanceApp/TransactionsView/TransactionsList.html', context)

    def add_transaction(request):
        pass

    def add_category(request):
        if request.method == 'POST':
            enterprise = request.user.enterprise_id
            user= request.user.id
            description = request.POST.dict()
            models.TransactionsCategories.add_category(enterprise, user, description)
            return redirect(resolve_url('Transactions'))
        else:
            return redirect(resolve_url('Transactions'))
    
class CategoriesView:
    def all_categories(request):
        return render(request, 'FinanceApp/TransactionsView/categories.html')

    