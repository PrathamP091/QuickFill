# Generated by Django 4.2.2 on 2023-06-16 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_product_out_of_stock_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('pending', 'Pending'), ('cancel', 'Cancel'), ('packed', 'Packed'), ('on the way', 'On The Way'), ('delivered', 'Delivered')], default='pending', max_length=50),
        ),
    ]
