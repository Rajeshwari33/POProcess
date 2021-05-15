# Generated by Django 3.2 on 2021-05-07 05:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetAllocated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('budget_allocated', models.CharField(max_length=128, null=True, verbose_name='Budget Allocated')),
                ('department', models.CharField(max_length=64, null=True, verbose_name='Department')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
            ],
            options={
                'db_table': 'budget_allocated',
            },
        ),
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('budget_category', models.CharField(max_length=128, null=True, verbose_name='Budget Category')),
                ('user_id', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
            ],
            options={
                'db_table': 'budget_category',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('location', models.CharField(max_length=128, null=True, verbose_name='Location')),
                ('user_id', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('prf_number', models.PositiveSmallIntegerField(null=True, verbose_name='PRF Number')),
                ('user_name', models.CharField(max_length=128, null=True, verbose_name='User Name')),
                ('location', models.CharField(max_length=128, null=True, verbose_name='Location')),
                ('requirement_date', models.DateTimeField(null=True, verbose_name='Requirement Date')),
                ('reporting_manager', models.CharField(max_length=128, null=True, verbose_name='Reporting Manager')),
                ('department', models.CharField(max_length=32, null=True, verbose_name='Department')),
                ('budget_allocated', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Budget Allocated')),
                ('is_budgeted', models.CharField(max_length=16, null=True, verbose_name='Budgeted Yes/No')),
                ('purpose', models.TextField(null=True, verbose_name='Purpose')),
                ('purchase_catagory', models.CharField(max_length=32, null=True, verbose_name='Purchase Catagory')),
                ('purchase_type', models.CharField(max_length=64, null=True, verbose_name='Type Of Purchase')),
                ('date_of_delivery_expected', models.DateTimeField(null=True, verbose_name='Date of Delivery Expected')),
                ('delivery_address', models.TextField(null=True, verbose_name='Delivery Expected')),
                ('benefits', models.TextField(null=True, verbose_name='Perceived Benefits')),
                ('total_line_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Total Line Value')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Is Processed ?')),
                ('po_status', models.BooleanField(default=False, verbose_name='PO Status')),
                ('is_dept_head_approved', models.BooleanField(default=False, verbose_name='Is Department Head Approved ?')),
                ('dept_head_approved_date', models.DateTimeField(null=True, verbose_name='Department Head Approved Date')),
                ('dept_head_approved_comments', models.TextField(null=True, verbose_name='Department Head Approved Comments')),
                ('is_approver_approved', models.BooleanField(default=False, verbose_name='Is Approver Approved ?')),
                ('approver_approved_date', models.DateTimeField(null=True, verbose_name='Approver Approved Date')),
                ('approver_approved_comments', models.TextField(null=True, verbose_name='Approver Approved Comments')),
                ('is_p2p_approved', models.BooleanField(default=False, verbose_name='Is P2P Approved ?')),
                ('p2p_approved_date', models.DateTimeField(null=True, verbose_name='P2P Approved Date')),
                ('p2p_approved_comments', models.TextField(null=True, verbose_name='P2P Approved Comments')),
                ('is_finance_approved', models.BooleanField(default=False, verbose_name='Is Finance Approved ?')),
                ('finance_approved_date', models.DateTimeField(null=True, verbose_name='Finance Approved Date')),
                ('finance_approved_comments', models.TextField(null=True, verbose_name='Finance Approved Comments')),
                ('is_po_issued', models.BooleanField(default=False, verbose_name=' Is PO Issued ?')),
                ('po_issued_date', models.DateTimeField(null=True, verbose_name='PO Issued Date')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
            ],
            options={
                'db_table': 'purchase_requirement',
            },
        ),
        migrations.CreateModel(
            name='QuotationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('prf_number', models.PositiveSmallIntegerField(null=True, verbose_name='PRF Number')),
                ('vendor_type', models.CharField(max_length=32, null=True, verbose_name='Vendor Type')),
                ('vendor_name', models.CharField(max_length=256, null=True, verbose_name='Vendor Name')),
                ('vendor_code', models.CharField(max_length=64, verbose_name='Vendor Code')),
                ('address', models.TextField(null=True, verbose_name='Address 1')),
                ('location', models.CharField(max_length=32, null=True, verbose_name='Location')),
                ('gst_number', models.CharField(max_length=15, null=True, verbose_name='GST Number')),
                ('pan_number', models.CharField(max_length=10, null=True, verbose_name='PAN Number')),
                ('total_line_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Total Line Value')),
                ('file_name', models.TextField(null=True, verbose_name='File Name')),
                ('quotation_path', models.TextField(null=True, verbose_name='Quotation Path')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
                ('purchase_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.purchaserequirement', verbose_name='Purchase Requirement Id')),
            ],
            options={
                'db_table': 'quotation_details',
            },
        ),
        migrations.CreateModel(
            name='ReportingManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('reporting_manager', models.CharField(max_length=128, null=True, verbose_name='Reporting Manager')),
                ('user_id', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
            ],
            options={
                'db_table': 'reporting_manager',
            },
        ),
        migrations.CreateModel(
            name='UniqueNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=32, verbose_name='Configuration Key')),
                ('description', models.TextField(verbose_name='Description')),
                ('type', models.CharField(max_length=32, verbose_name='User Type')),
                ('expression', models.CharField(max_length=32, verbose_name='Expression')),
                ('value', models.PositiveIntegerField(verbose_name='Value')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
            ],
            options={
                'db_table': 'unique_number',
            },
        ),
        migrations.CreateModel(
            name='VendorMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('vendor_code', models.CharField(max_length=64, verbose_name='Vendor Code')),
                ('Location', models.CharField(max_length=32, null=True, verbose_name='Location')),
                ('vendor_name', models.CharField(max_length=256, null=True, verbose_name='Vendor Name')),
                ('address', models.TextField(null=True, verbose_name='Address 1')),
                ('gst_number', models.CharField(max_length=15, null=True, verbose_name='GST Number')),
                ('pan_number', models.CharField(max_length=10, null=True, verbose_name='PAN Number')),
                ('status', models.CharField(max_length=16, null=True, verbose_name='Status')),
                ('email_id', models.CharField(max_length=128, null=True, verbose_name='Email Id')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
            ],
            options={
                'db_table': 'vendor_master',
            },
        ),
        migrations.CreateModel(
            name='VendorSupportingDocuments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('file_1_name', models.TextField(null=True, verbose_name='File 1 Name')),
                ('file_1_path', models.TextField(null=True, verbose_name='File 1 Path')),
                ('file_2_name', models.TextField(null=True, verbose_name='File 2 Name')),
                ('file_2_path', models.TextField(null=True, verbose_name='File 2 Path')),
                ('file_3_name', models.TextField(null=True, verbose_name='File 3 Name')),
                ('file_3_path', models.TextField(null=True, verbose_name='File 3 Path')),
                ('file_4_name', models.TextField(null=True, verbose_name='File 4 Name')),
                ('file_4_path', models.TextField(null=True, verbose_name='File 4 Path')),
                ('file_5_name', models.TextField(null=True, verbose_name='File 5 Name')),
                ('file_5_path', models.TextField(null=True, verbose_name='File 5 Path')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
                ('purchase_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.purchaserequirement', verbose_name='Purchase Requirement Id')),
                ('quotation_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.quotationdetails', verbose_name='Quotation Details Id')),
            ],
            options={
                'db_table': 'vendor_supporting_documents',
            },
        ),
        migrations.CreateModel(
            name='QuotationLineDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('prf_number', models.PositiveSmallIntegerField(null=True, verbose_name='PRF Number')),
                ('material_name', models.TextField(null=True, verbose_name='Material/Service Name')),
                ('line_description', models.TextField(null=True, verbose_name='Line Description')),
                ('quantity', models.PositiveIntegerField(null=True, verbose_name='Quantity')),
                ('unit_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Unit Value')),
                ('total_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Total Value')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
                ('purchase_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.purchaserequirement', verbose_name='Purchase Requirement Id')),
                ('quotation_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.quotationdetails', verbose_name='Quotation Details Id')),
            ],
            options={
                'db_table': 'quotation_line_details',
            },
        ),
        migrations.CreateModel(
            name='LineDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_id', models.PositiveSmallIntegerField(null=True, verbose_name='Tenant Id')),
                ('group_id', models.PositiveSmallIntegerField(null=True, verbose_name='Group Id')),
                ('entity_id', models.PositiveSmallIntegerField(null=True, verbose_name='Entity Id')),
                ('module_id', models.PositiveSmallIntegerField(null=True, verbose_name='Module Id')),
                ('prf_number', models.PositiveSmallIntegerField(null=True, verbose_name='PRF Number')),
                ('material_name', models.TextField(null=True, verbose_name='Material/Service Name')),
                ('budget_category', models.CharField(max_length=128, null=True, verbose_name='Budget Category')),
                ('line_description', models.TextField(null=True, verbose_name='Line Description')),
                ('quantity', models.PositiveIntegerField(null=True, verbose_name='Quantity')),
                ('unit_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Unit Value')),
                ('total_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Total Value')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created Date')),
                ('modified_by', models.PositiveSmallIntegerField(null=True, verbose_name='User Id')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified Date')),
                ('uploaded_by', models.CharField(max_length=64, null=True, verbose_name='User Name')),
                ('purchase_requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.purchaserequirement', verbose_name='Purchase Requirement Id')),
            ],
            options={
                'db_table': 'line_details',
            },
        ),
    ]
