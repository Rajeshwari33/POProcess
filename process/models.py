from django.db import models
from django.utils import timezone


class PurchaseRequirement(models.Model):
    class Meta:
        db_table = "purchase_requirement"

    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    prf_number = models.CharField(max_length=64, verbose_name="PRF Number", null=True)
    user_name = models.CharField(max_length=128, verbose_name="User Name", null=True)
    location = models.CharField(max_length=128, verbose_name="Location", null=True)
    requirement_date = models.DateTimeField(verbose_name="Requirement Date", null=True)
    reporting_manager = models.CharField(max_length=128, verbose_name="Reporting Manager", null=True)
    department = models.CharField(max_length=32, verbose_name="Department", null=True)
    budget_allocated = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Budget Allocated", default=0.00)
    is_budgeted = models.CharField(max_length=16, verbose_name="Budgeted Yes/No", null=True)
    purpose = models.TextField(verbose_name="Purpose", null=True)
    purchase_catagory = models.CharField(max_length=32, verbose_name="Purchase Catagory", null=True)
    purchase_type = models.CharField(max_length=64, verbose_name="Type Of Purchase", null=True)
    date_of_delivery_expected = models.DateTimeField(verbose_name="Date of Delivery Expected", null=True)
    delivery_address = models.TextField(verbose_name="Delivery Expected", null=True)
    benefits = models.TextField(verbose_name="Perceived Benefits", null=True)
    total_line_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Line Value", default=0.00)
    finalized_vendor = models.CharField(max_length=255, verbose_name="Finalized Vendor", null=True)
    is_processed = models.IntegerField(default=False, verbose_name="Is Processed ?")
    po_status = models.CharField(max_length=128, verbose_name="PO Status", null=True)
    is_dept_head_approved = models.IntegerField(default=False, verbose_name="Is Department Head Approved ?")
    dept_head_approved_date = models.DateTimeField(verbose_name="Department Head Approved Date", null=True)
    dept_head_approved_comments = models.TextField(verbose_name="Department Head Approved Comments", null=True)
    is_approver_approved = models.IntegerField(default=False, verbose_name="Is Approver Approved ?")
    approver_approved_date = models.DateTimeField(verbose_name="Approver Approved Date", null=True)
    approver_approved_comments = models.TextField(verbose_name="Approver Approved Comments", null=True)
    is_p2p_approved = models.IntegerField(default=False, verbose_name="Is P2P Approved ?")
    p2p_approved_date = models.DateTimeField(verbose_name="P2P Approved Date", null=True)
    p2p_approved_comments = models.TextField(verbose_name="P2P Approved Comments", null=True)
    is_finance_approved = models.IntegerField(default=False, verbose_name="Is Finance Approved ?")
    finance_approved_date = models.DateTimeField(verbose_name="Finance Approved Date", null=True)
    finance_approved_comments = models.TextField(verbose_name="Finance Approved Comments", null=True)
    is_po_issued = models.BooleanField(default=False, verbose_name=" Is PO Issued ?")
    po_issued_date = models.DateTimeField(verbose_name="PO Issued Date", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class LineDetails(models.Model):
    class Meta:
        db_table = "line_details"

    purchase_requirement = models.ForeignKey(PurchaseRequirement, verbose_name="Purchase Requirement Id", on_delete=models.CASCADE)
    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    prf_number = models.CharField(max_length=64, verbose_name="PRF Number", null=True)
    material_name = models.TextField(verbose_name="Material/Service Name", null=True)
    budget_category = models.CharField(max_length=128, verbose_name="Budget Category", null=True)
    line_description = models.TextField(verbose_name="Line Description", null=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity", null=True)
    unit_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Unit Value", default=0.00)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Value", default=0.00)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class QuotationDetails(models.Model):
    class Meta:
        db_table = "quotation_details"

    purchase_requirement = models.ForeignKey(PurchaseRequirement, verbose_name="Purchase Requirement Id", on_delete=models.CASCADE)
    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    prf_number = models.CharField(max_length=64, verbose_name="PRF Number", null=True)
    vendor_type = models.CharField(max_length=32, verbose_name="Vendor Type", null=True)
    vendor_name = models.CharField(max_length=256, verbose_name="Vendor Name", null=True)
    vendor_code = models.CharField(max_length=64, verbose_name="Vendor Code", null=False)
    address = models.TextField(verbose_name="Address 1", null=True)
    location = models.CharField(max_length=32, verbose_name="Location", null=True)
    gst_number = models.CharField(max_length=15, verbose_name="GST Number", null=True)
    pan_number = models.CharField(max_length=10, verbose_name="PAN Number", null=True)
    total_line_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Line Value", default=0.00)
    quotationfile_name = models.TextField(verbose_name="Quotation File Name", null=True)
    VendorFile_name = models.TextField(verbose_name="Vendor File Name", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class QuotationLineDetails(models.Model):
    class Meta:
        db_table = "quotation_line_details"

    purchase_requirement = models.ForeignKey(PurchaseRequirement, verbose_name="Purchase Requirement Id", on_delete=models.CASCADE)
    quotation_details = models.ForeignKey(QuotationDetails, verbose_name="Quotation Details Id", on_delete=models.CASCADE)
    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    vendor_name = models.CharField(max_length=256, verbose_name="Vendor Name", null=True)
    prf_number = models.CharField(max_length=64, verbose_name="PRF Number", null=True)
    material_name = models.TextField(verbose_name="Material/Service Name", null=True)
    line_description = models.TextField(verbose_name="Line Description", null=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity", null=True)
    unit_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Unit Value", default=0.00)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Value", default=0.00)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class VendorSupportingDocuments(models.Model):
    class Meta:
        db_table = "vendor_supporting_documents"

    purchase_requirement = models.ForeignKey(PurchaseRequirement, verbose_name="Purchase Requirement Id", on_delete=models.CASCADE)
    quotation_details = models.ForeignKey(QuotationDetails, verbose_name="Quotation Details Id", on_delete=models.CASCADE)
    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    file_1_name = models.TextField(verbose_name="File 1 Name", null=True)
    file_1_path = models.TextField(verbose_name="File 1 Path", null=True)
    file_2_name = models.TextField(verbose_name="File 2 Name", null=True)
    file_2_path = models.TextField(verbose_name="File 2 Path", null=True)
    file_3_name = models.TextField(verbose_name="File 3 Name", null=True)
    file_3_path = models.TextField(verbose_name="File 3 Path", null=True)
    file_4_name = models.TextField(verbose_name="File 4 Name", null=True)
    file_4_path = models.TextField(verbose_name="File 4 Path", null=True)
    file_5_name = models.TextField(verbose_name="File 5 Name", null=True)
    file_5_path = models.TextField(verbose_name="File 5 Path", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class VendorMaster(models.Model):
    class Meta:
        db_table = "vendor_master"

    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    vendor_code = models.CharField(max_length=64, verbose_name="Vendor Code", null=False)
    Location = models.CharField(max_length=32, verbose_name="Location", null=True)
    vendor_name = models.CharField(max_length=256, verbose_name="Vendor Name", null=True)
    address = models.TextField(verbose_name="Address 1", null=True)
    gst_number = models.CharField(max_length=15, verbose_name="GST Number", null=True)
    pan_number = models.CharField(max_length=10, verbose_name="PAN Number", null=True)
    status = models.CharField(max_length=16, verbose_name="Status", null=True)
    email_id = models.CharField(max_length=128, verbose_name="Email Id", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class ReportingManager(models.Model):
    class Meta:
        db_table = "reporting_manager"

    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    reporting_manager = models.CharField(max_length=128, verbose_name="Reporting Manager", null=True)
    user_id = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class BudgetCategory(models.Model):
    class Meta:
        db_table = "budget_category"

    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    budget_category = models.CharField(max_length=128, verbose_name="Budget Category", null=True)
    user_id = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class Location(models.Model):
    class Meta:
        db_table = "location"

    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    location = models.CharField(max_length=128, verbose_name="Location", null=True)
    address = models.TextField(verbose_name="Address 1", null=True)
    user_id = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class BudgetAllocated(models.Model):
    class Meta:
        db_table = "budget_allocated"

    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    budget_allocated = models.CharField(max_length=128, verbose_name="Budget Allocated", null=True)
    department = models.CharField(max_length=64, verbose_name="Department", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)

class UniqueNumber(models.Model):
    class Meta:
        db_table = "unique_number"

    key = models.CharField(max_length=32, verbose_name="Configuration Key", null=False)
    description = models.TextField(verbose_name="Description")
    type = models.CharField(max_length=32, verbose_name="User Type", null=False)
    expression = models.CharField(max_length=32, verbose_name="Expression", null=False)
    value = models.TextField(verbose_name="Value", null=False)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")

class UploadFiles(models.Model):
    class Meta:
        db_table = "upload_files"

    purchase_requirement = models.ForeignKey(PurchaseRequirement, verbose_name="Purchase Requirement Id", on_delete=models.CASCADE)
    quotation_details = models.ForeignKey(QuotationDetails, verbose_name="Quotation Details Id", on_delete=models.CASCADE)
    tenant_id = models.PositiveSmallIntegerField(verbose_name="Tenant Id", null=True)
    group_id = models.PositiveSmallIntegerField(verbose_name="Group Id", null=True)
    entity_id = models.PositiveSmallIntegerField(verbose_name="Entity Id", null=True)
    module_id = models.PositiveSmallIntegerField(verbose_name="Module Id", null=True)
    prf_number = models.CharField(max_length=64, verbose_name="PRF Number", null=True)
    category = models.CharField(max_length=128, verbose_name="Category", null=True)
    file_type = models.CharField(max_length=128, verbose_name="File Type", null=True)
    file_path = models.TextField(verbose_name="File Path", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Created Date")
    modified_by = models.PositiveSmallIntegerField(verbose_name="User Id", null=True)
    modified_date = models.DateTimeField(default=timezone.now, verbose_name="Modified Date")
    uploaded_by = models.CharField(max_length=64, verbose_name="User Name", null=True)
