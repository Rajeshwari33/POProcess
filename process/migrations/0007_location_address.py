# Generated by Django 3.2 on 2021-05-10 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0006_purchaserequirement_finalized_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='address',
            field=models.TextField(null=True, verbose_name='Address 1'),
        ),
    ]