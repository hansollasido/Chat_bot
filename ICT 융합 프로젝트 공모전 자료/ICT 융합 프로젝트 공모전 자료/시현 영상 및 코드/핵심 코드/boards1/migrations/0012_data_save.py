# Generated by Django 4.0.3 on 2022-03-10 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards1', '0011_data_csv2_delete_data_csv_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='data_save',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_q', models.CharField(max_length=1000)),
                ('d_a', models.CharField(max_length=1000)),
            ],
        ),
    ]
