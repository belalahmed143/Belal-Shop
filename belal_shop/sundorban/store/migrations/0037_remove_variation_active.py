# Generated by Django 3.2.8 on 2022-02-28 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0036_remove_variation_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='active',
        ),
    ]
