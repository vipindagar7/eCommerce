# Generated by Django 4.2.6 on 2024-04-12 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_orderitem_color_orderitem_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='color',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
