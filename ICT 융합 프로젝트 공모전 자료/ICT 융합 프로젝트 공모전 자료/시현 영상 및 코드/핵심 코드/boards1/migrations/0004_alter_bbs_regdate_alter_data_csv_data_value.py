# Generated by Django 4.0.3 on 2022-03-07 17:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards1', '0003_data_csv_alter_bbs_regdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bbs',
            name='regdate',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 7, 17, 34, 59, 200811)),
        ),
        migrations.AlterField(
            model_name='data_csv',
            name='data_value',
            field=models.CharField(max_length=1000),
        ),
    ]
