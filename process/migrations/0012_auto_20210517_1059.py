# Generated by Django 3.2 on 2021-05-17 05:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0011_auto_20210514_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotationdetails',
            name='pan_number',
        ),
        migrations.AddField(
            model_name='quotationdetails',
            name='mail_id',
            field=models.CharField(max_length=10, null=True, verbose_name='Mail Id'),
        ),
        migrations.AlterField(
            model_name='purchaserequirement',
            name='date_of_delivery_expected',
            field=models.CharField(max_length=128, null=True, verbose_name='Date of Delivery Expected'),
        ),
        migrations.CreateModel(
            name='POFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('prf_number', models.CharField(max_length=64, null=True, verbose_name='PRF Number')),
                ('category', models.CharField(max_length=128, null=True, verbose_name='Category')),
                ('file_type', models.CharField(max_length=128, null=True, verbose_name='File Type')),
                ('file_path', models.TextField(null=True, verbose_name='File Path')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
                ('purchase_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.purchaserequirement', verbose_name='Purchase Requirement Id')),
            ],
            options={
                'db_table': 'po_files',
            },
        ),
    ]
