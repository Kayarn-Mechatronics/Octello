from django.db import models, utils
from datetime import *
from AssetsApp.models import Assets, AssetsCategories
from django.core import serializers
# Create your models here.
class Accounts(Assets):
    #Accounts are regarded as special type of asses
    class Meta:
        proxy=True
    
    @classmethod
    def add_account(self, description):
        asset_id = "OCASS-{0}".format(self.objects.count()+ 1)
        try:
            self.objects.create(
                asset_id = asset_id,
                name = description["account_name"],
                category = AssetsCategories.objects.get(id=1),
                sub_category = AssetsCategories.objects.get(id=2),#int(description["sub_category"]),
                description = description["description"],
                class_term = description['class'],
                currency = description["currency"],
                status = description["status"],
                datetime_added = datetime.now()
                )
            return asset_id
        except utils.IntegrityError:
            return False
        except utils.OperationalError:
            return False
    @classmethod  
    def to_json(self):
        accounts_list = []
        for item in self.objects.filter(category=1):
            description = {"account_id" : item.asset_id}
            description['sub_category'] = item.sub_category.name
            description["name"] = item.name
            description["description"] = item.description
            description["currency"] = item.currency
            description["status"] = item.status
            accounts_list.append(description)
        
        return  accounts_list
    
    @classmethod
    def starting_balance(self, account_id, balance_flow, balance, currency):
        #If Balance is smaller than zero
        if balance_flow == 0:
            data = {'from_account' : account_id}
            data['category'] = 1
            data['sub-category'] = 3
            data['from_amount'] = balance
            data['from_currency'] = currency
            data['fees'] = 0
            data['attachments'] = None
            data['user_id'] = None
            data['fees'] = None
            data['budget_id'] = None
            data['comments'] = None
            TransactionsDB.outbound(data)
            
        elif balance_flow ==  1:
            data = {'to_account' : account_id}
            data['category'] = 1
            data['sub-category'] = 3
            data['to_amount'] = balance
            data['to_currency'] = currency
            data['fees'] = 0
            data['attachments'] = None
            data['user_id'] = None
            data['fees'] = None
            data['budget_id'] = None
            data['comments'] = None
            TransactionsDB.inbound(data)
        else:
            pass

class TransactionsDB(models.Model):
    transaction_id = models.CharField(primary_key=True, max_length=15, unique=True, editable=False) 
    datetime_stamp = models.DateTimeField()
    type = models.CharField(max_length=20, blank=False)
    from_account = models.CharField(max_length=30, null=True, blank=False)
    to_account = models.CharField(max_length=30, null=True, blank=False)
    category = models.CharField(max_length=50, null=True,blank=False)
    sub_category = models.CharField(max_length=50, null=True, blank=False)
    from_amount = models.PositiveBigIntegerField(null=True, blank=False)
    from_currency = models.CharField(max_length=5, null=True, blank=False)
    to_amount = models.PositiveBigIntegerField(null=True, blank=False)
    to_currency = models.CharField(max_length=5, null=True, blank=False)
    fees = models.CharField(max_length=30, null=True, blank=False)
    exchange_rate = models.PositiveBigIntegerField(null=True, blank=False )
    comments = models.TextField(null=True, blank=True)
    attachments = models.FilePathField(allow_folders=True, allow_files=True, null=True)
    user_posted = models.CharField(max_length=40, null=True)
    budget_id = models.CharField(max_length=40, null=True)
    
    @classmethod
    def inbound(self, data):
        self.objects.create(
            transaction_id = "OCFIN-TR{}".format(self.objects.count()+ 1), 
            datetime_stamp = datetime.now(),
            type = "Inbound",
            to_account = data['to_account'],
            category = data['category'],
            sub_category = data['sub-category'],
            to_amount = data['to_amount'],
            to_currency = data['to_currency'],
            comments = data['comments'],
            attachments = data['attachments'],
            user_posted = data['user_id'],
            fees = data['fees'],
            budget_id = data['budget_id']
        )   
    
    @classmethod
    def outbound(self, data):
        self.objects.create(
            transaction_id = "OCFIN-TR{}".format(self.objects.count()+ 1), 
            datetime_stamp = datetime.now(),
            type = "Outbound",
            from_account = data['from_account'],
            category = data['category'],
            sub_category = data['sub-category'],
            from_amount = data['from_amount'],
            from_currency = data['from_currency'],
            comments = data['comments'],
            attachments = data['attachments'],
            user_posted = data['user_id'],
            fees = data['fees'],
            budget_id = data['budget_id']
        )   
    @classmethod
    def to_json(self):
        obj =  serializers.serialize('json', self.objects.all())
        
          
class Categories(models.Model):
    id = models.PositiveIntegerField(primary_key=True, editable=False)
    flow_type = models.CharField(max_length=40) #distinguish btn Income & Expense
    parent_id = models.PositiveIntegerField(null=True)
    description = models.CharField(max_length=40, blank=False)
    comment = models.TextField(blank=True, null=True)
    is_sub_category = models.BooleanField()
    
#emmanuelbienvenue10@gmail.com