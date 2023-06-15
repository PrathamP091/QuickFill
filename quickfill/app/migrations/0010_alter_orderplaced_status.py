# Generated by Django 4.2.2 on 2023-06-15 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_payment_orderplaced'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('packed', 'Packed'), ('pending', 'Pending'), ('on the way', 'On The Way'), ('delivered', 'Delivered'), ('cancel', 'Cancel')], default='ending', max_length=50),
        ),
    ]
