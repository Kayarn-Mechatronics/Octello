from django.core.serializers import serialize
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from . import models
from datetime import *

# Create your views here.
class AccountsView:
    def all_accounts(request):
        print(serialize('json', models.Accounts.objects.all()))
        context = {'accounts_list' : models.Accounts.to_json()}
        context['total_accounts'] = len(context['accounts_list'])
        return render(request, 'FinanceApp/Accounts/Accounts.html', context)
    
    def add_account(request):
        if request.method == 'POST':
            account_id = models.Accounts.add_account(request.POST.dict())
            if account_id != False:
                if int(request.POST.dict()['balance']) != 0:
                    #print(type(account_id))
                    models.Accounts.starting_balance(account_id, int(request.POST.dict()['balance_flow']),int(request.POST.dict()['balance']), request.POST.dict()['currency'])
                    return redirect(resolve_url('Accounts'))
                else:
                    return redirect(resolve_url('Accounts'))
            else:
                return redirect(resolve_url('Accounts'))
        else:
            return redirect(resolve_url('Accounts'))
        
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
    
class CategoriesView:
    def all_categories(request):
        return render(request, 'FinanceApp/TransactionsView/categories.html')