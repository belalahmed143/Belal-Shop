# Generated by Django 3.2.8 on 2022-03-16 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paymentApp', '0005_alter_billingaddress_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='default',
        ),
    ]
