# Generated by Django 3.2.8 on 2022-03-13 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='order_note',
            field=models.TextField(),
        ),
    ]