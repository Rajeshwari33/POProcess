# Generated by Django 3.2 on 2021-05-08 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_auto_20210507_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uniquenumber',
            name='value',
            field=models.TextField(verbose_name='Value'),
        ),
    ]