# Generated by Django 3.2.5 on 2021-08-19 23:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AssetsApp', '0004_auto_20210820_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetscategories',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 20, 1, 45, 39, 668719)),
        ),
        migrations.RemoveField(
            model_name='assetscategories',
            name='parent_id',
        ),
        migrations.AddField(
            model_name='assetscategories',
            name='parent_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
