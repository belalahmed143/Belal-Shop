# Generated by Django 3.2.8 on 2022-02-15 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20220216_0211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categoris',
        ),
        migrations.AddField(
            model_name='product',
            name='categoris',
            field=models.ManyToManyField(to='store.ProductCategory', verbose_name='Product Category'),
        ),
    ]
