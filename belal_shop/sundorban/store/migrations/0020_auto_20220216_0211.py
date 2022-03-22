# Generated by Django 3.2.8 on 2022-02-15 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_productimggallery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categoris',
        ),
        migrations.AddField(
            model_name='product',
            name='categoris',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.productcategory', verbose_name='Product Category'),
        ),
    ]