# Generated by Django 3.1.3 on 2022-02-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20220214_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='delivery_address_latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivery_address_longitude',
            field=models.FloatField(default=0),
        ),
    ]
