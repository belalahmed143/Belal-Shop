# Generated by Django 3.2.8 on 2022-03-11 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0040_whishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='whishlist',
            old_name='product',
            new_name='wish_product',
        ),
    ]