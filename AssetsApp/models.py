from django.db import models
from datetime import *
from django import utils


# Create your models here. 
class AssetsCategories(models.Model):
    id = models.PositiveIntegerField(primary_key=True, editable=False)
    parent_id = models.PositiveIntegerField(null=True,)
    name = models.CharField(max_length=40, blank=False)
    description = models.TextField(blank=True, null=True)
    is_sub_category = models.BooleanField()
    datetime_added = models.DateTimeField(default=datetime.now())
    
    class Meta:
        db_tablespace = 'Assets'
    
    @classmethod    
    def add_category(self, description):
        self.objects.create(id=self.objects.count() + 1,
                            name = description['name'], 
                            description = description['description'],
                            is_sub_category = 0,
                            datetime_added = datetime.now()
                            )
    @classmethod 
    def add_sub_category(self, description):
        self.objects.create(id=self.objects.count() + 1,
                            parent_id = int(description['category']),
                            name = description['name'],
                            description = description['description'],
                            is_sub_category = 1,
                            datetime_added = datetime.now()
                            )
      
class Assets(models.Model):
    asset_id = models.CharField(max_length=20, primary_key=True, editable=False)
    category = models.ForeignKey(AssetsCategories, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(AssetsCategories, on_delete=models.CASCADE, related_name='sub_category')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    class_term = models.CharField(max_length=15)
    status = models.CharField(max_length=20, help_text='0 Is Inservice, 1 is Inactive and 3 Under Maintaince' )
    currency = models.CharField(max_length=5, null=True)
    datetime_added = models.DateTimeField(auto_now=True)
    #item_id = models.ForeignKey(Items, on_delete=models.CASCADE, null=True)
        
    class Meta:
        db_tablespace = 'Assets'
        
    @classmethod
    def add_asset(self, description):
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