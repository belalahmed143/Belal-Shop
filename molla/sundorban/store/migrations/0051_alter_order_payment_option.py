# Generated by Django 3.2.8 on 2022-03-16 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0050_auto_20220316_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_option',
            field=models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('SSL Commerce', 'SSL Commerce'), ('Stripe', 'Stripe'), ('PayPal', 'PayPal')], max_length=150),
        ),
    ]
