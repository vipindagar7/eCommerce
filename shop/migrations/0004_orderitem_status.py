# Generated by Django 4.2.6 on 2024-03-31 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_orderitem_address_orderitem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]
