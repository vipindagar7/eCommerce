# Generated by Django 4.2.6 on 2024-03-30 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerprofile',
            name='alt_phone',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='phone',
            field=models.IntegerField(unique=True),
        ),
    ]
