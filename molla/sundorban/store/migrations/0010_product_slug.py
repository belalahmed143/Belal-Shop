# Generated by Django 3.2.8 on 2022-02-12 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_productcategory_top_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=3),
        ),
    ]
