# Generated by Django 3.1.3 on 2022-02-17 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20220215_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='store_restaurant_address',
            field=models.CharField(default='', max_length=255),
        ),
    ]
