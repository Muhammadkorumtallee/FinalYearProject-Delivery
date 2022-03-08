# Generated by Django 3.1.3 on 2022-03-06 17:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_delivery_delivery_rate_charge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='receipt_number',
        ),
        migrations.AddField(
            model_name='delivery',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
