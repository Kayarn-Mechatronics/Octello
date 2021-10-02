from django.db import models, utils
from datetime import *
import AuthenticationApp
from django.core import serializers
# Create your models here.

class AccountsCategories(models.Model):
    enterprise_id = models.ForeignKey(AuthenticationApp.models.Enterprises, on_delete=models.CASCADE)
    id = models.PositiveIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=40, blank=False)
    description = models.TextField(blank=True, null=True)
    datetime_added = models.DateTimeField()
    user = models.ForeignKey(AuthenticationApp.models.User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'FinanceApp_AccountsCategories'
    
    @classmethod    
    def add_category(self, enterprise, user, description):
        self.objects.create(id=self.objects.count() + 1,
                            enterprise_id = AuthenticationApp.models.Enterprises.objects.get(enterprise_id=enterprise),
                            name = description['category_name'], 
                            description = description['description'],
                            datetime_added = datetime.now(),
                            user = AuthenticationApp.models.User.objects.get(id=user)
                            )
    @classmethod
    def categories(self, enterprise):
        return  self.objects.filter(enterprise_id = AuthenticationApp.models.Enterprises.objects.get(enterprise_id=enterprise)
                                    )



class Accounts(models.Model):
    #Accounts are regarded as special type of asses
    enterprise_id = models.ForeignKey(AuthenticationApp.models.Enterprises, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=20, primary_key=True, editable=False)
    category = models.ForeignKey(AccountsCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    class_term = models.CharField(max_length=50)
    status = models.CharField(max_length=20, help_text='0 Is Inservice, 1 is Inactive and 3 Under Maintaince' )
    currency = models.CharField(max_length=5, null=True)
    datetime_added = models.DateTimeField(auto_now=True)
        
    class Meta:
        db_table = 'FinanceApp_Accounts'
    
    @classmethod
    def add_account(self, enterprise, user, description):
        account_id = "OCASS-{0}".format(self.objects.count()+ 1)
        try:
            self.objects.create(
                enterprise_id = AuthenticationApp.models.Enterprises.objects.get(enterprise_id=enterprise),
                account_id = account_id,
                name = description["account_name"],
                category = AccountsCategories.objects.get(id=1),
                description = description["description"],
                class_term = description['class'],
                currency = description["currency"],
                status = description["status"],
                datetime_added = datetime.now()
                )
            return account_id
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
    def starting_balance(self, enterprise, user, data):
        #If Balance is smaller than zero
        if data['balance_flow'] == 0:
            # data = {'from_account' : description['account_id']}
            # data['category'] = 1
            # data['sub-category'] = 3
            # data['from_amount'] = balance
            # data['from_currency'] = currency
            # data['fees'] = 0
            # data['attachments'] = None
            # data['user_id'] = None
            # data['fees'] = None
            # data['budget_id'] = None
            # data['comments'] = None
            TransactionsDB.outbound(enterprise, user, data)
            
        elif data['balance_flow'] ==  1:
            # data = {'to_account' : account_id}
            # data['category'] = 1
            # data['sub-category'] = 3
            # data['to_amount'] = balance
            # data['to_currency'] = currency
            # data['fees'] = 0
            # data['attachments'] = None
            # data['user_id'] = None
            # data['fees'] = None
            # data['budget_id'] = None
            # data['comments'] = None
            TransactionsDB.inbound(enterprise, user, data)
        else:
            pass

          
class TransactionsCategories(models.Model):
    enterprise_id = models.ForeignKey(AuthenticationApp.models.Enterprises, on_delete=models.CASCADE)
    id = models.PositiveIntegerField(primary_key=True, editable=False)
    flow_type = models.SmallIntegerField() #distinguish btn Income & Expense
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=40, blank=False)
    description = models.TextField(blank=True, null=True)
    is_sub_category = models.BooleanField()
    datetime_added = models.DateTimeField()
    user_id = models.ForeignKey(AuthenticationApp.models.User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'FinanceApp_TransactionsCategories'

    @classmethod    
    def add_category(self, enterprise, user, description): 
        self.objects.create(id=self.objects.count() + 1,
                            enterprise_id = AuthenticationApp.models.Enterprises.objects.get(enterprise_id=enterprise),
                            flow_type = int(description['class']),
                            name = description['category_name'], 
                            description = description['description'],
                            is_sub_category = 0,
                            datetime_added = datetime.now(),
                            user_id = AuthenticationApp.models.User.objects.get(id=user)
                            )
    
    @classmethod 
    def add_sub_category(self, enterprise, user, description):
        self.objects.create(id=self.objects.count() + 1,
                            enterprise_id = AuthenticationApp.models.Enterprises.objects.get(enterprise_id=enterprise),
                            parent_id = self.objects.get(id=description['category_id']),
                            flow_type = -1,
                            name = description['category_name'],
                            description = description['description'],
                            is_sub_category = 1,
                            datetime_added = datetime.now(),
                            user_id = AuthenticationApp.models.User.objects.get(id=user)
                            )
 

class TransactionsDB(models.Model):
    enterprise_id = models.ForeignKey(AuthenticationApp.models.Enterprises, on_delete=models.CASCADE)
    transaction_id = models.CharField(primary_key=True, max_length=15, unique=True, editable=False) 
    datetime_stamp = models.DateTimeField()
    type = models.SmallIntegerField()
    from_account = models.ForeignKey(Accounts, null=True, blank=True, on_delete=models.CASCADE, related_name='from_account')
    to_account = models.ForeignKey(Accounts, null=True, blank=True, on_delete=models.CASCADE, related_name='to_account')
    category = models.ForeignKey(TransactionsCategories, null=True,blank=False, on_delete=models.CASCADE, related_name='category')
    sub_category = models.ForeignKey(TransactionsCategories, null=True, blank=False, on_delete=models.CASCADE, related_name='sub_category')
    from_amount = models.PositiveBigIntegerField(null=True, blank=False)
    from_currency = models.CharField(max_length=5, null=True, blank=False)
    to_amount = models.PositiveBigIntegerField(null=True, blank=False)
    to_currency = models.CharField(max_length=5, null=True, blank=False)
    fees = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    exchange_rate = models.PositiveBigIntegerField(null=True, blank=False )
    comments = models.TextField(null=True, blank=True)
    attachments = models.FilePathField(allow_folders=True, allow_files=True, null=True)
    user = models.ForeignKey(AuthenticationApp.models.User, on_delete=models.CASCADE)
    budget_id = models.CharField(max_length=40, null=True)

    class Meta:
        db_table = 'FinanceApp_Transactions'
    
    @classmethod
    def inbound(self, enterprise, user, data):
        self.objects.create(
            enterprise_id = AuthenticationApp.models.Enterprises.objects.get(enterprise_id=enterprise),
            transaction_id = "OCFIN-TR{}".format(self.objects.count()+ 1), 
            datetime_stamp = datetime.now(),
            type = "Inbound",
            to_account = Accounts.objects.get(account_id=data['to_account']),
            category = TransactionsCategories.objects.get(id=data['category']),
            sub_category = TransactionsCategories.objects.get(id=data['sub_category']),
            to_amount = data['to_amount'],
            to_currency = data['to_currency'],
            comments = data['comments'],
            attachments = data['attachments'],
            user =  AuthenticationApp.models.User.objects.get(id=user),
            fees = data['fees'],
            budget_id = data['budget_id']
        )   
    
    @classmethod
    def outbound(self, enterprise, user, data):
        self.objects.create(
            enterprise_id = AuthenticationApp.models.Enterprises.objects.get(enterprise_id=enterprise),
            transaction_id = "OCFIN-TR{}".format(self.objects.count()+ 1), 
            datetime_stamp = datetime.now(),
            type = "Outbound",
            from_account = Accounts.objects.get(account_id=data['from_account']),
            category = TransactionsCategories.objects.get(id=data['category']),
            sub_category = TransactionsCategories.objects.get(id=data['sub_category']),
            from_amount = data['from_amount'],
            from_currency = data['from_currency'],
            comments = data['comments'],
            attachments = data['attachments'],
            user = AuthenticationApp.models.User.objects.get(id=user),
            fees = data['fees'],
            budget_id = data['budget_id']
        ) 
                           