# Generated by Django 3.2 on 2021-05-08 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0004_auto_20210508_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfiles',
            name='uploaded_by',
            field=models.CharField(max_length=64, null=True, verbose_name='User Name'),
        ),
    ]