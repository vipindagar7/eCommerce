# Generated by Django 4.2.6 on 2024-03-30 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_userprofile_address_alter_userprofile_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_seller',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
