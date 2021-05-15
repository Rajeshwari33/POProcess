from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse
import json
import logging
from datetime import datetime
from django.db import connection
import pandas as pd

logger = logging.getLogger("po_process")

def execute_sql_query(query, object_type):
    try:
        with connection.cursor() as cursor:
            logger.info("Executing SQL Query..")
            logger.info(query)

            cursor.execute(query)
            if object_type == "table":
                column_names = [col[0] for col in cursor.description]
                rows = dict_fetch_all(cursor)
                table_output = {"headers":column_names, "data":rows}
                output = json.dumps(table_output)
                return output
            elif object_type in["update", "create"]:
                return None
            else:
                rows = cursor.fetchall()
                column_header = [col[0] for col in cursor.description]
                df = pd.DataFrame(rows)
                return [df, column_header]

    except Exception as e:
        logger.info("Error Executing SQL Query!!", exc_info=True)
        return None

def dict_fetch_all(cursor):
    "Return all rows from cursor as a dictionary"
    try:
        column_header = [col[0] for col in cursor.description]
        return [dict(zip(column_header, row)) for row in cursor.fetchall()]
    except Exception as e:
        logger.error("Error in converting cursor data to dictionary", exc_info=True)

@csrf_exempt
def get_user_details(request,*args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)

            user_id = ''
            user_name = ''

            for k,v in data.items():
                if k == "user_name":
                    user_name = v
                if k == "user_id":
                    user_id = v
                if k == "department":
                    department = v

            # reporting_manager = []
            # budget_category = []
            # allocated_budget = []
            if len(str(user_name)) > 0:
                if len(str(user_id)) > 0:
                    user_name_changed = user_name[0:2]
                    # print(user_name_changed)

                    value = UniqueNumber.objects.filter(key='uniqueNumber')

                    for values in value:
                        number = values.value
                        expression = values.expression
                        # print(number)
                        # print(expression)

                    prf_number = expression + str(number) + user_name_changed + "-T"

                    manager = ReportingManager.objects.filter(user_id=user_id)
                    for user in manager:
                        reporting_manager = user.reporting_manager

                    budget = BudgetCategory.objects.filter(user_id=user_id)
                    for category in budget:
                        budget_category = category.budget_category

                    locations = Location.objects.filter(is_active=1)
                    location_names = []
                    for location in locations:
                        location_names.append(location.location)

                    budget_allocation = BudgetAllocated.objects.filter(department=department)
                    for budget in budget_allocation:
                        allocated_budget = budget.budget_allocated

                    return JsonResponse ({
                        "reporting_manager" : reporting_manager,
                        "budget_category" : budget_category,
                        "allocated_budget" : allocated_budget,
                        "prf_number" : prf_number,
                        "location" : location_names
                    })
                else :
                    return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
            else :
                return JsonResponse({"status": "Error", "Message": "User Name Not Found!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting user details", exc_info=True)
        return JsonResponse({"status": "Error"})

@csrf_exempt
def get_location_details(request,*args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)

            for k,v in data.items():
                if k == "location_name":
                    location_name = v

            if len(location_name) > 0:
                items = Location.objects.filter(location = location_name)

                for item in items:
                    address = item.address

                return JsonResponse({
                    "address" : address
                })
            else:
                return JsonResponse({"Status": "Error", "Message": "Location Name Not Found!!!"})
        else:
            return JsonResponse({"Status": "Error", "Message": "POST Method Not Received!!!"})

    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Vendor Details", exc_info=True)
        return JsonResponse({"status": "Error"})

@csrf_exempt
def get_vendor_name(request,*args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)

            for k,v in data.items():
                if k == "vendor_type":
                    vendor_type = v

            if vendor_type == "Existing":
                vendors = VendorMaster.objects.filter(is_active = 1)
                vendor_names = []
                for vendor in vendors:
                    vendor_names.append(vendor.vendor_name)
                # print(vendor_names)

                return JsonResponse({"vendor_name" : vendor_names})
        else:
            return JsonResponse({"Status": "Error", "Message": "POST Method Not Received!!!"})

    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Vendor Name", exc_info=True)
        return JsonResponse({"status": "Error"})

@csrf_exempt
def get_vendor_details(request,*args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)

            for k,v in data.items():
                if k == "vendor_name":
                    vendor_name = v

            if len(vendor_name) > 0:
                vendors = VendorMaster.objects.filter(vendor_name = vendor_name)

                for vendor in vendors:
                    vendor_code = vendor.vendor_code
                    Location = vendor.Location
                    address = vendor.address
                    gst_number = vendor.gst_number
                    pan_number = vendor.pan_number

                return JsonResponse({
                    "vendor_code" : vendor_code,
                    "Location" : Location,
                    "address" : address,
                    "gst_number" : gst_number,
                    "pan_number" : pan_number
                })
            else:
                return JsonResponse({"Status": "Error", "Message": "Vendor Name Not Found!!!"})
        else:
            return JsonResponse({"Status": "Error", "Message": "POST Method Not Received!!!"})

    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Vendor Details", exc_info=True)
        return JsonResponse({"status": "Error"})

@csrf_exempt
def get_prf_details(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "prf_number":
                    prf_number = v
                if k == "user_name":
                    user_name = v
                if k == "location":
                    location = v
                if k == "requirement_date":
                    requirement_date = v
                if k == "reporting_manager":
                    reporting_manager = v
                if k == "department":
                    department = v
                if k == "budget_allocated":
                    budget_allocated = v
                if k == "is_budgeted":
                    is_budgeted = v
                if k == "purpose":
                    purpose = v
                if k == "purchase_catagory":
                    purchase_catagory = v
                if k == "purchase_type":
                    purchase_type = v
                if k == "date_of_delivery_expected":
                    date_of_delivery_expected = v
                if k == "delivery_address":
                    delivery_address = v
                if k == "perceived_benefits":
                    benefits = v
                if k == "total_line_value":
                    total_line_value = v
                if k == "finalized_vendor":
                    finalized_vendor = v
                if k == "porequirementinfo":
                    porequirementinfo_list = v
                if k == "poquotation":
                    poquotation = v

            reqirement_details = PurchaseRequirement(
                tenant_id = tenant_id,
                group_id = group_id,
                entity_id = entity_id,
                module_id = module_id,
                prf_number = prf_number,
                user_name = user_name,
                location = location,
                requirement_date = requirement_date,
                reporting_manager = reporting_manager,
                department = department,
                budget_allocated = budget_allocated,
                is_budgeted = is_budgeted,
                purpose = purpose,
                purchase_catagory = purchase_catagory,
                purchase_type = purchase_type,
                date_of_delivery_expected = date_of_delivery_expected,
                delivery_address = delivery_address,
                benefits = benefits,
                total_line_value = total_line_value,
                finalized_vendor = finalized_vendor,
                is_active=1,
                created_by=user_id,
                created_date=timezone.now(),
                modified_by=user_id,
                modified_date=timezone.now(),
                uploaded_by=user_name
            )
            reqirement_details.save()

            details = PurchaseRequirement.objects.filter(prf_number=prf_number)
            for detail in details:
                requirement_id = detail.id

            for value in porequirementinfo_list:
                for k,v in value.items():
                    if k == "material_name":
                        material_name = v
                    if k == "budget_category":
                        budget_category = v
                    if k == "line_description":
                        line_description = v
                    if k == "quantity":
                        quantity = v
                    if k == "unit_value":
                        unit_value = v
                    if k == "total_value":
                        total_value = v

                line_details = LineDetails(
                    tenant_id= tenant_id,
                    group_id= group_id,
                    entity_id= entity_id,
                    module_id= module_id,
                    prf_number=prf_number,
                    material_name = material_name,
                    budget_category = budget_category,
                    line_description = line_description,
                    quantity = quantity,
                    unit_value = unit_value,
                    total_value = total_value,
                    is_active=1,
                    created_by=user_id,
                    created_date=timezone.now(),
                    modified_by=user_id,
                    modified_date=timezone.now(),
                    purchase_requirement_id = requirement_id,
                    uploaded_by=user_name
                )
                line_details.save()

            for values in poquotation:
                for k,v in values.items():
                    if k == "vendor_type":
                        vendor_type = v
                    if k == "vendor_name":
                        vendor_name = v
                    if k == "vendor_code":
                        vendor_code = v
                    if k == "vendor_address":
                        address = v
                    if k == "vendor_location":
                        vendor_location = v
                    if k == "gst_number":
                        gst_number = v
                    if k == "pan_number":
                        pan_number = v
                    if k == "vendor_total_line_value":
                        vendor_total_line_value = v
                    if k == "quotationfile_name":
                        quotationfile_name = v
                    if k == "VendorFile_name":
                        VendorFile_name = v
                    if k == "poquotationinfo":
                        poquotationinfo = v

                quotation_details = QuotationDetails(
                    tenant_id=tenant_id,
                    group_id=group_id,
                    entity_id=entity_id,
                    module_id=module_id,
                    prf_number=prf_number,
                    vendor_type=vendor_type,
                    vendor_name=vendor_name,
                    vendor_code=vendor_code,
                    address=address,
                    location=vendor_location,
                    gst_number=gst_number,
                    pan_number=pan_number,
                    total_line_value=vendor_total_line_value,
                    quotationfile_name=quotationfile_name,
                    VendorFile_name=VendorFile_name,
                    is_active=1,
                    created_by=user_id,
                    created_date=timezone.now(),
                    modified_by=user_id,
                    modified_date=timezone.now(),
                    purchase_requirement_id=requirement_id,
                    uploaded_by=user_name
                )
                quotation_details.save()

                details = QuotationDetails.objects.filter(prf_number=prf_number)
                for detail in details:
                    quotation_id = detail.id

                for value in poquotationinfo:
                    for k,v in value.items():
                        if k == "vendor_material_name":
                            vendor_material_name = v
                        if k == "vendor_line_description":
                            vendor_line_description = v
                        if k == "vendor_quantity":
                            vendor_quantity = v
                        if k == "vendor_unit_value":
                            vendor_unit_value = v
                        if k == "vendor_total_value":
                            vendor_total_value = v

                    quotation_line_details = QuotationLineDetails(
                        tenant_id=tenant_id,
                        group_id=group_id,
                        entity_id=entity_id,
                        module_id=module_id,
                        prf_number=prf_number,
                        vendor_name=vendor_name,
                        material_name=vendor_material_name,
                        line_description=vendor_line_description,
                        quantity=vendor_quantity,
                        unit_value=vendor_unit_value,
                        total_value=vendor_total_value,
                        purchase_requirement_id=requirement_id,
                        is_active=1,
                        created_by=user_id,
                        created_date=timezone.now(),
                        modified_by=user_id,
                        modified_date=timezone.now(),
                        quotation_details_id=quotation_id,
                        uploaded_by=user_name
                    )
                    quotation_line_details.save()

            value = UniqueNumber.objects.filter(key='uniqueNumber')
            for values in value:
                values.value = int(values.value) + 1
                values.save()

            return JsonResponse({"status" : "Sucess", "Message" : "Data Uploaded Successfully!!!"})
        else:
            return JsonResponse({"Status" : "Error", "Message" : "POST Method Not Received!!!"})
            
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting PRF details", exc_info=True)
        return JsonResponse({"status" : "Error"})

@csrf_exempt
def get_file_upload(request, *args,**kwargs):
    try:
        if request.method == "POST":
            tenant_id = request.POST.get("tenant_id")
            if tenant_id is not None:
                group_id = request.POST.get("group_id")
                if group_id is not None:
                    entity_id = request.POST.get("entity_id")
                    if entity_id is not None:
                        user_id = request.POST.get("user_id")
                        if user_id is not None:
                            user_name = request.POST.get("user_name")
                            if user_name is not None:
                                module_id = request.POST.get("module_id")
                                if module_id is not None:
                                    prf_number = request.POST.get("prf_number")
                                    if prf_number is not None:
                                        file_name = request.FILES["QuotationFile"].name
                                        file_name_extension = "." + file_name.split(".")[-1]
                                        file_name_without_extension = file_name.replace(file_name_extension, "")
                                        file_name_proper = file_name_without_extension.replace(".", "") + "_" + str(datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "_").replace(".", "_") + file_name_extension
                                        file_name_proper = file_name_proper.replace(" ", "_").replace("-", "_").replace("'","").replace( "#", "_No_").replace("&", "_").replace("(", "_").replace(")", "_")
                                        file_type = file_name.split(".")[-1]

                                        details = PurchaseRequirement.objects.filter(prf_number=prf_number)
                                        for detail in details:
                                            requirement_id = detail.id

                                        details = QuotationDetails.objects.filter(prf_number=prf_number)
                                        for detail in details:
                                            quotation_id = detail.id

                                        if file_type in ["PDF", "Pdf", "pdf"]:
                                            items = UniqueNumber.objects.filter(key='uploadFolder', expression='pdf')
                                            for item in items:
                                                file_path = item.value

                                            file_upload_path_name_date = file_path + file_name_proper

                                            with open(file_upload_path_name_date, 'wb+') as destination:
                                                for chunk in request.FILES["QuotationFile"]:
                                                    destination.write(chunk)

                                            upload_files = UploadFiles.objects.create(
                                                tenant_id = tenant_id,
                                                group_id = group_id,
                                                entity_id = entity_id,
                                                module_id = module_id,
                                                prf_number = prf_number,
                                                category = "Quotation",
                                                file_type = file_type,
                                                file_path = file_upload_path_name_date,
                                                is_active=1,
                                                created_by=user_id,
                                                created_date=timezone.now(),
                                                modified_by=user_id,
                                                modified_date=timezone.now(),
                                                uploaded_by=user_name,
                                                purchase_requirement_id = requirement_id,
                                                quotation_details_id = quotation_id
                                            )
                                            upload_files.save()

                                        elif file_type in ["jpg", "png"]:
                                            items = UniqueNumber.objects.filter(key='uploadFolder', expression='Image')
                                            for item in items:
                                                file_path = item.value

                                            file_upload_path_name_date = file_path + file_name_proper

                                            with open(file_upload_path_name_date, 'wb+') as destination:
                                                for chunk in request.FILES["QuotationFile"]:
                                                    destination.write(chunk)

                                            upload_files = UploadFiles.objects.create(
                                                tenant_id=tenant_id,
                                                group_id=group_id,
                                                entity_id=entity_id,
                                                module_id=module_id,
                                                prf_number=prf_number,
                                                category="Quotation",
                                                file_type=file_type,
                                                file_path=file_upload_path_name_date,
                                                is_active=1,
                                                created_by=user_id,
                                                created_date=timezone.now(),
                                                modified_by=user_id,
                                                modified_date=timezone.now(),
                                                uploaded_by=user_name,
                                                purchase_requirement_id = requirement_id,
                                                quotation_details_id = quotation_id
                                            )
                                            upload_files.save()

                                        return JsonResponse({"Status": "Success", "Message" : "File Uploaded Successfully!!!"})
                                    else:
                                        return JsonResponse({"Status" : "Error", "Message": "PRF Number Not Found!!!"})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Name Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status": "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting File Upload", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# To get PRF list
@csrf_exempt
def get_user_prf_list(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "department":
                    department = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if department is not None:
                                    query = "SELECT IFNULL(TRIM(id), '') AS 'requirement_id', IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status' FROM po_process.purchase_requirement WHERE created_by = '{user_id}' AND department = '{department}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_query = query.replace("{user_id}", str(user_id)).replace("{department}", str(department)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    return JsonResponse({"Status": "Success", "data": query_output["data"]})
                                else:
                                    return JsonResponse({"Status" : "Error", "Message" : "Department Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status" : "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting User PRF List", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# To Get prf form and quotaion fields
@csrf_exempt
def get_prf_form_input_fields(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "requirement_id":
                    requirement_id = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:
                                    query = "SELECT IFNULL(TRIM(id), '') AS 'requirement_id', IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status' FROM po_process.purchase_requirement WHERE created_by = '{user_id}' AND id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_query = query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    line_query = "SELECT IFNULL(TRIM(id), '') AS 'poreqinfo_id', IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(budget_category), '') AS 'budget_category', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_line_query = line_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    line_query_output = json.loads(execute_sql_query(final_line_query, object_type="table"))
                                    quotation_query = "SELECT IFNULL(TRIM(id), '') AS 'pobudget_id', IFNULL(TRIM(vendor_type), '') AS 'vendor_type', IFNULL(TRIM(vendor_name), '') AS 'vendor_name', IFNULL(TRIM(vendor_code), '') AS 'vendor_code', IFNULL(TRIM(address), '') AS 'address', IFNULL(TRIM(location), '') AS 'location', IFNULL(TRIM(gst_number), '') AS 'gst_number', IFNULL(TRIM(pan_number), '') AS 'pan_number', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value' FROM po_process.quotation_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_quotation_query = quotation_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_query_output = json.loads(execute_sql_query(final_quotation_query, object_type="table"))
                                    quotation_line_query = "SELECT IFNULL(TRIM(id), '') AS 'pobudgetinfo_id', IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.quotation_line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_quotation_line_query = quotation_line_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_line_query_output = json.loads(execute_sql_query(final_quotation_line_query, object_type="table"))
                                    poquotation_dict = {
                                        "prf_list" : query_output["data"],
                                        "requirement_info" : line_query_output["data"],
                                        "quotation_fields" : quotation_query_output["data"],
                                        "quotation_requirement_info" : quotation_line_query_output["data"]
                                    }
                                    return JsonResponse({"Status": "Success", "data": poquotation_dict})
                                else:
                                    return JsonResponse({"Status" : "Error", "Message" : "Department Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status" : "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting PRF Form fields", exc_info=True)
        return JsonResponse({"Status" : "Error"})

@csrf_exempt
def get_edit_prf_form_details(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "prf_number":
                    prf_number = v
                if k == "user_name":
                    user_name = v
                if k == "location":
                    location = v
                if k == "requirement_date":
                    requirement_date = v
                if k == "reporting_manager":
                    reporting_manager = v
                if k == "department":
                    department = v
                if k == "budget_allocated":
                    budget_allocated = v
                if k == "is_budgeted":
                    is_budgeted = v
                if k == "purpose":
                    purpose = v
                if k == "purchase_catagory":
                    purchase_catagory = v
                if k == "purchase_type":
                    purchase_type = v
                if k == "date_of_delivery_expected":
                    date_of_delivery_expected = v
                if k == "delivery_address":
                    delivery_address = v
                if k == "perceived_benefits":
                    benefits = v
                if k == "total_line_value":
                    total_line_value = v
                if k == "finalized_vendor":
                    finalized_vendor = v
                if k == "porequirementinfo":
                    porequirementinfo_list = v
                if k == "poquotation":
                    poquotation_list = v
                if k == "requirement_id":
                    requirement_id = v
            # print(poquotation_list)

            prf_details = PurchaseRequirement.objects.filter(id = requirement_id, tenant_id = tenant_id, group_id = group_id, entity_id = entity_id, module_id = module_id)

            for details in prf_details:
                details.prf_number = prf_number
                details.user_name = user_name
                details.location = location
                details.requirement_date = requirement_date
                details.reporting_manager = reporting_manager
                details.department = department
                details.budget_allocated = budget_allocated
                details.is_budgeted = is_budgeted
                details.purpose = purpose
                details.purchase_catagory = purchase_catagory
                details.purchase_type = purchase_type
                details.date_of_delivery_expected = date_of_delivery_expected
                details.delivery_address = delivery_address
                details.benefits = benefits
                details.total_line_value = total_line_value
                details.finalized_vendor = finalized_vendor
                details.save()

            for value in porequirementinfo_list:
                for k,v in value.items():
                    if k == "material_name":
                        material_name = v
                    if k == "budget_category":
                        budget_category = v
                    if k == "line_description":
                        line_description = v
                    if k == "quantity":
                        quantity = v
                    if k == "unit_value":
                        unit_value = v
                    if k == "total_value":
                        total_value = v
                    if k == "poreqinfo_id":
                        line_id = v
                    # print(line_id)

                items = LineDetails.objects.filter(id = line_id, tenant_id = tenant_id, group_id = group_id, entity_id = entity_id, module_id = module_id)

                for item in items:
                    item.prf_number = prf_number
                    item.material_name = material_name
                    item.budget_category = budget_category
                    item.line_description = line_description
                    item.quantity = quantity
                    item.unit_value = unit_value
                    item.total_value = total_value
                    item.save()

            for values in poquotation_list:
                for k,v in values.items():
                    if k == "vendor_type":
                        vendor_type = v
                    if k == "vendor_name":
                        vendor_name = v
                    if k == "vendor_code":
                        vendor_code = v
                    if k == "vendor_address":
                        address = v
                    if k == "vendor_location":
                        vendor_location = v
                    if k == "gst_number":
                        gst_number = v
                    if k == "pan_number":
                        pan_number = v
                    if k == "vendor_total_line_value":
                        vendor_total_line_value = v
                    if k == "quotationfile_name":
                        quotationfile_name = v
                    if k == "VendorFile_name":
                        VendorFile_name = v
                    if k == "pobudget_id":
                        quotation_id = v
                    if k == "poquotationinfo":
                        poquotationinfo_list = v
                # print(quotation_id)
                # print(k,v)

                quotations = QuotationDetails.objects.filter(id = quotation_id, tenant_id = tenant_id, group_id = group_id, entity_id = entity_id, module_id = module_id)

                for quotation in quotations:
                    quotation.prf_number = prf_number
                    quotation.vendor_type = vendor_type
                    quotation.vendor_name = vendor_name
                    quotation.vendor_code = vendor_code
                    quotation.address = address
                    quotation.vendor_location = vendor_location
                    quotation.gst_number = gst_number
                    quotation.pan_number = pan_number
                    quotation.vendor_total_line_value = vendor_total_line_value
                    quotation.quotationfile_name = quotationfile_name
                    quotation.VendorFile_name = VendorFile_name
                    quotation.save()

                for value in poquotationinfo_list:
                    for k, v in value.items():
                        if k == "vendor_material_name":
                            vendor_material_name = v
                        if k == "vendor_line_description":
                            vendor_line_description = v
                        if k == "vendor_quantity":
                            vendor_quantity = v
                        if k == "vendor_unit_value":
                            vendor_unit_value = v
                        if k == "vendor_total_value":
                            vendor_total_value = v
                        if k == "pobudgetinfo_id":
                            quotation_line_id = v
                    # print(quotation_line_id)

                    values = QuotationLineDetails.objects.filter(id = quotation_line_id, tenant_id = tenant_id, group_id = group_id, entity_id = entity_id, module_id = module_id)

                    for value in values:
                        value.prf_number = prf_number
                        value.vendor_material_name = vendor_material_name
                        value.vendor_line_description = vendor_line_description
                        value.vendor_quantity = vendor_quantity
                        value.vendor_unit_value = vendor_unit_value
                        value.vendor_total_value = vendor_total_value
                        value.save()

            return JsonResponse({"status" : "Success", "Message" : "Data Uploaded Successfully!!!"})

        else:
            return JsonResponse({"status" : "Error", "Message" : "POST Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Edit PRF Form Details", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# To get Department Head PRF list
@csrf_exempt
def get_dept_head_prf_list(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "department":
                    department = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if department is not None:
                                    query = "SELECT IFNULL(TRIM(id), '') AS 'requirement_id', IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status' FROM po_process.purchase_requirement WHERE is_processed = 1 AND department = '{department}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_query = query.replace("{department}", str(department)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    return JsonResponse({"Status": "Success", "data": query_output["data"]})
                                else:
                                    return JsonResponse({"Status" : "Error", "Message" : "Department Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status" : "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Department Head PRF List", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# To Get Department Head prf form and quotaion fields
@csrf_exempt
def get_dept_head_prf_form_input_fields(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "requirement_id":
                    requirement_id = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:
                                    query = "SELECT IFNULL(TRIM(id), '') AS 'requirement_id', IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status' FROM po_process.purchase_requirement WHERE is_processed = 1 AND id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_query = query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    line_query = "SELECT IFNULL(TRIM(id), '') AS 'poreqinfo_id', IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(budget_category), '') AS 'budget_category', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_line_query = line_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    line_query_output = json.loads(execute_sql_query(final_line_query, object_type="table"))
                                    quotation_query = "SELECT IFNULL(TRIM(id), '') AS 'pobudget_id', IFNULL(TRIM(vendor_type), '') AS 'vendor_type', IFNULL(TRIM(vendor_name), '') AS 'vendor_name', IFNULL(TRIM(vendor_code), '') AS 'vendor_code', IFNULL(TRIM(address), '') AS 'address', IFNULL(TRIM(location), '') AS 'location', IFNULL(TRIM(gst_number), '') AS 'gst_number', IFNULL(TRIM(pan_number), '') AS 'pan_number', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value' FROM po_process.quotation_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_quotation_query = quotation_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_query_output = json.loads(execute_sql_query(final_quotation_query, object_type="table"))
                                    quotation_line_query = "SELECT IFNULL(TRIM(id), '') AS 'pobudgetinfo_id', IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.quotation_line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_quotation_line_query = quotation_line_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_line_query_output = json.loads(execute_sql_query(final_quotation_line_query, object_type="table"))
                                    poquotation_dict = {
                                        "prf_list" : query_output["data"],
                                        "requirement_info" : line_query_output["data"],
                                        "quotation_fields" : quotation_query_output["data"],
                                        "quotation_requirement_info" : quotation_line_query_output["data"]
                                    }
                                    return JsonResponse({"Status": "Success", "data": poquotation_dict})
                                else:
                                    return JsonResponse({"Status" : "Error", "Message" : "Department Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status" : "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Department Head PRF Form fields", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# Deprtment Head Functionality
@csrf_exempt
def dept_head_functionality(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k, v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "requirement_id":
                    requirement_id = v
                if k == "is_dept_head_approved":
                    is_dept_head_approved = v
                if k == "remarks":
                    remarks = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:

                                    orders = PurchaseRequirement.objects.filter(id=requirement_id, tenant_id=tenant_id, group_id=group_id, entity_id=entity_id, module_id=module_id)

                                    if is_dept_head_approved == 1:
                                        for order in orders:
                                            order.is_dept_head_approved = is_dept_head_approved
                                            order.po_status = "APPROVED BY DEPARTMENT HEAD"
                                            order.dept_head_approved_date = timezone.now()
                                            order.dept_head_approved_comments = remarks
                                            order.save()

                                    elif is_dept_head_approved == 2:
                                        for order in orders:
                                            order.is_dept_head_approved = is_dept_head_approved
                                            order.po_status = "HOLD BY DEPARTMENT HEAD"
                                            order.dept_head_approved_date = timezone.now()
                                            order.dept_head_approved_comments = remarks
                                            order.save()

                                    elif is_dept_head_approved == 3:
                                        for order in orders:
                                            order.is_dept_head_approved = is_dept_head_approved
                                            order.po_status = "REJECTED BY DEPARTMENT HEAD"
                                            order.dept_head_approved_date = timezone.now()
                                            order.dept_head_approved_comments = remarks
                                            order.save()

                                    elif is_dept_head_approved == 4:
                                        for order in orders:
                                            order.is_dept_head_approved = is_dept_head_approved
                                            order.po_status = "SENT TO BUDGET APPROVAL"
                                            order.dept_head_approved_date = timezone.now()
                                            order.dept_head_approved_comments = remarks
                                            order.save()
                                    return JsonResponse({"Status": "Success", "Message": "Updated Successfully"})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Requirement Id Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status": "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Department Head Functionality", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# To get P2P Team PRF list
@csrf_exempt
def get_p2p_team_prf_list(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                query = "SELECT IFNULL(TRIM(id), '') AS 'requirement_id', IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                final_query = query.replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                return JsonResponse({"Status": "Success", "data": query_output["data"]})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status" : "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting P2P Team PRF List", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# To Get P2P Team prf form and quotaion fields
@csrf_exempt
def get_p2p_team_prf_form_input_fields(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "requirement_id":
                    requirement_id = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:
                                    query = "SELECT IFNULL(TRIM(id), '') AS 'requirement_id', IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_query = query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    line_query = "SELECT IFNULL(TRIM(id), '') AS 'poreqinfo_id', IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(budget_category), '') AS 'budget_category', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_line_query = line_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    line_query_output = json.loads(execute_sql_query(final_line_query, object_type="table"))
                                    quotation_query = "SELECT IFNULL(TRIM(id), '') AS 'pobudget_id', IFNULL(TRIM(vendor_type), '') AS 'vendor_type', IFNULL(TRIM(vendor_name), '') AS 'vendor_name', IFNULL(TRIM(vendor_code), '') AS 'vendor_code', IFNULL(TRIM(address), '') AS 'address', IFNULL(TRIM(location), '') AS 'location', IFNULL(TRIM(gst_number), '') AS 'gst_number', IFNULL(TRIM(pan_number), '') AS 'pan_number', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value' FROM po_process.quotation_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_quotation_query = quotation_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_query_output = json.loads(execute_sql_query(final_quotation_query, object_type="table"))
                                    quotation_line_query = "SELECT IFNULL(TRIM(id), '') AS 'pobudgetinfo_id', IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.quotation_line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_quotation_line_query = quotation_line_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_line_query_output = json.loads(execute_sql_query(final_quotation_line_query, object_type="table"))
                                    poquotation_dict = {
                                        "prf_list" : query_output["data"],
                                        "requirement_info" : line_query_output["data"],
                                        "quotation_fields" : quotation_query_output["data"],
                                        "quotation_requirement_info" : quotation_line_query_output["data"]
                                    }
                                    return JsonResponse({"Status": "Success", "data": poquotation_dict})
                                else:
                                    return JsonResponse({"Status" : "Error", "Message" : "Department Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status" : "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting P2P Team PRF Form fields", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# P2P Team Functionality
@csrf_exempt
def p2p_team_functionality(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k, v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "requirement_id":
                    requirement_id = v
                if k == "is_p2p_approved":
                    is_p2p_approved = v
                if k == "remarks":
                    remarks = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:

                                    orders = PurchaseRequirement.objects.filter(id=requirement_id, tenant_id=tenant_id, group_id=group_id, entity_id=entity_id, module_id=module_id)

                                    if is_p2p_approved == 1:
                                        for order in orders:
                                            order.is_p2p_approved = is_p2p_approved
                                            order.po_status = "APPROVED BY P2P TEAM"
                                            order.p2p_approved_date = timezone.now()
                                            order.p2p_approved_comments = remarks
                                            order.save()

                                    elif is_p2p_approved == 2:
                                        for order in orders:
                                            order.is_p2p_approved = is_p2p_approved
                                            order.po_status = "HOLD BY P2P TEAM"
                                            order.p2p_approved_date = timezone.now()
                                            order.p2p_approved_comments = remarks
                                            order.save()

                                    elif is_p2p_approved == 3:
                                        for order in orders:
                                            order.is_p2p_approved = is_p2p_approved
                                            order.po_status = "REJECTED BY P2P TEAM"
                                            order.p2p_approved_date = timezone.now()
                                            order.p2p_approved_comments = remarks
                                            order.save()

                                    return JsonResponse({"Status": "Success", "Message": "Updated Successfully"})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Requirement Id Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status": "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in P2P Team Functionality", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# To get Finance PRF list
@csrf_exempt
def get_finance_prf_list(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                query = "SELECT IFNULL(TRIM(id), '') AS 'requirement_id', IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND is_p2p_approved = 1 AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                final_query = query.replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                return JsonResponse({"Status": "Success", "data": query_output["data"]})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status" : "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Finance PRF List", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# To Get Finance prf form and quotaion fields
@csrf_exempt
def get_finance_prf_form_input_fields(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k,v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "requirement_id":
                    requirement_id = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:
                                    query = "SELECT IFNULL(TRIM(id), '') AS 'requirement_id', IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND is_p2p_approved = 1 AND id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_query = query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    line_query = "SELECT IFNULL(TRIM(id), '') AS 'poreqinfo_id', IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(budget_category), '') AS 'budget_category', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_line_query = line_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    line_query_output = json.loads(execute_sql_query(final_line_query, object_type="table"))
                                    quotation_query = "SELECT IFNULL(TRIM(id), '') AS 'pobudget_id', IFNULL(TRIM(vendor_type), '') AS 'vendor_type', IFNULL(TRIM(vendor_name), '') AS 'vendor_name', IFNULL(TRIM(vendor_code), '') AS 'vendor_code', IFNULL(TRIM(address), '') AS 'address', IFNULL(TRIM(location), '') AS 'location', IFNULL(TRIM(gst_number), '') AS 'gst_number', IFNULL(TRIM(pan_number), '') AS 'pan_number', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value' FROM po_process.quotation_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_quotation_query = quotation_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_query_output = json.loads(execute_sql_query(final_quotation_query, object_type="table"))
                                    quotation_line_query = "SELECT IFNULL(TRIM(id), '') AS 'pobudgetinfo_id', IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.quotation_line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}';"
                                    final_quotation_line_query = quotation_line_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_line_query_output = json.loads(execute_sql_query(final_quotation_line_query, object_type="table"))
                                    poquotation_dict = {
                                        "prf_list" : query_output["data"],
                                        "requirement_info" : line_query_output["data"],
                                        "quotation_fields" : quotation_query_output["data"],
                                        "quotation_requirement_info" : quotation_line_query_output["data"]
                                    }
                                    return JsonResponse({"Status": "Success", "data": poquotation_dict})
                                else:
                                    return JsonResponse({"Status" : "Error", "Message" : "Department Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status" : "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Finance PRF Form fields", exc_info=True)
        return JsonResponse({"Status" : "Error"})

# Finance Functionality
@csrf_exempt
def finance_functionality(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            user_id = ''

            for k, v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v
                if k == "user_id":
                    user_id = v
                if k == "requirement_id":
                    requirement_id = v
                if k == "is_finance_approved":
                    is_finance_approved = v
                if k == "remarks":
                    remarks = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:

                                    orders = PurchaseRequirement.objects.filter(id=requirement_id, tenant_id=tenant_id, group_id=group_id, entity_id=entity_id, module_id=module_id)

                                    if is_finance_approved == 1:
                                        for order in orders:
                                            order.is_finance_approved = is_finance_approved
                                            order.po_status = "APPROVED BY FINANCE"
                                            order.finance_approved_date = timezone.now()
                                            order.finance_approved_comments = remarks
                                            order.save()

                                    elif is_finance_approved == 2:
                                        for order in orders:
                                            order.is_finance_approved = is_finance_approved
                                            order.po_status = "HOLD BY FINANCE"
                                            order.finance_approved_date = timezone.now()
                                            order.finance_approved_comments = remarks
                                            order.save()

                                    elif is_finance_approved == 3:
                                        for order in orders:
                                            order.is_finance_approved = is_finance_approved
                                            order.po_status = "REJECTED BY FINANCE"
                                            order.finance_approved_date = timezone.now()
                                            order.finance_approved_comments = remarks
                                            order.save()

                                    return JsonResponse({"Status": "Success", "Message": "Updated Successfully"})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Requirement Id Not Found!!!"})
                            else:
                                return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
                        else:
                            return JsonResponse({"Status": "Error", "Message": "Module Id Not Found!!!"})
                    else:
                        return JsonResponse({"Status": "Error", "Message": "Entity Id Not Found!!!"})
                else:
                    return JsonResponse({"Status": "Error", "Message": "Group Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "Tenant Id Not Found!!!"})
        else:
            return JsonResponse({"Status": "Error", "Message": "Post Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Finance Functionality", exc_info=True)
        return JsonResponse({"Status" : "Error"})