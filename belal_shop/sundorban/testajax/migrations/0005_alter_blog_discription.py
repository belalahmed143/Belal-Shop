# Generated by Django 3.2.8 on 2022-02-21 18:34

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('testajax', '0004_auto_20220221_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='discription',
            field=tinymce.models.HTMLField(),
        ),
    ]
