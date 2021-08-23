from django.db import models
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField

# Create your models here.
class WizzardsDB(models.Model):
    wizzard_id = models.SmallIntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=80, null=False, unique=True)
    description = models.TextField(null=False, max_length=100)
    author = models.CharField(max_length=40,null=False)
    source = models.CharField(max_length=40)
    requests = models.PositiveIntegerField(null=False)
    rating = models.PositiveIntegerField()
    created = models.DateTimeField()
    last_update = models.DateTimeField()
    verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(null=True)
    

class WizzardRatting(models.Model):
    wizzard_id = models.ForeignKey(WizzardsDB, on_delete=models.CASCADE)
    rating_id = models.PositiveBigIntegerField()
    rating = models.PositiveSmallIntegerField()
    user_id = models.CharField(max_length=50, unique=True, null=True)
    date_stamp = models.DateField()
    time_stamp = models.TimeField()

class WizzardComment(models.Model):
    wizzard_id = models.ForeignKey(WizzardsDB, on_delete=models.CASCADE)
    commend_id = models.PositiveBigIntegerField(unique=True)
    user_id = models.CharField(max_length=50)
    comment_text = models.TextField(null=False, blank=False)
    date_stamp = models.DateField(null=False)
    time_stamp = models.TimeField(null=False)
    last_update = models.DateTimeField()
    
    def by_wizzard(self, wizzard_id):
        self.objects.filter(wizzard_id=wizzard_id)