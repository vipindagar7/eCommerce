# Generated by Django 4.2.6 on 2024-04-02 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_cart_seller_orderitem_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
