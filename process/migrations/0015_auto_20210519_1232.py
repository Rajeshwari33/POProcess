# Generated by Django 3.2 on 2021-05-19 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0014_vendorfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaserequirement',
            name='payment_term',
            field=models.CharField(max_length=255, null=True, verbose_name='Payment Term'),
        ),
        migrations.AddField(
            model_name='purchaserequirement',
            name='po_file_name',
            field=models.TextField(null=True, verbose_name='PO File Name'),
        ),
        migrations.DeleteModel(
            name='VendorFiles',
        ),
    ]
