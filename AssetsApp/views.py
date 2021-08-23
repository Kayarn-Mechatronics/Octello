from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from . import models
from datetime import *

# Create your views here.
class AssetsView:
    def all_assets(request):
        context = {'assets_list' : models.Assets.to_json()}
        context['total_assets'] = len(context['assets_list'])
        return render(request, 'AssetsApp/AssetsView/Assets.html', context)
    
    def add_asset(request):
        if request.method == 'POST':
            description = request.POST.dict()
            assets_db = models.Assets
            asset_id = assets_db.add_asset(description)
            if asset_id != False:
                if description['balance'] != '0':
                    assets_db.starting_balance(asset_id, int(description['balance']), description['currency'])
                    return redirect(resolve_url('Assets'))
                else:
                    return redirect(resolve_url('Assets'))
            else:
                return redirect(resolve_url('Assets'))
        else:
            return redirect(resolve_url('Assets'))
        
    def lookup(request):
        if request.method == 'GET':
            return HttpResponse(True)
        
    def add_category(request):
        if request.method == 'POST':
            models.AssetsCategories.add_category(request.POST.dict())
            return redirect(resolve_url('Assets'))
        
    def statement(request, asset_id):
        print(asset_id)
        return render(request, 'AssetsApp/AssetsView/statements.html')  
    
     
class TransactionView:
    def all_transactions(request):
        return render(request, 'AssetsApp/transactions/transactions.html')
   