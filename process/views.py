
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse
import json
import logging
from datetime import datetime
from django.db import connection
import pandas as pd
from .send_mail import resend_approved_mail

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
                table_output = {"headers": column_names, "data": rows}
                output = json.dumps(table_output)
                return output
            elif object_type in ["update", "create"]:
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
def get_user_details(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)

            user_id = ''
            user_name = ''

            for k, v in data.items():
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

                    # budget = BudgetCategory.objects.filter(user_id=user_id)
                    # for category in budget:
                    #     budget_category = category.budget_category

                    query = "SELECT id AS 'location_id', IFNULL(TRIM(location), '') AS 'location', IFNULL(TRIM(address), '') AS 'delivery_address' FROM po_process.location WHERE is_active = 1;"
                    query_output = json.loads(execute_sql_query(query, object_type="table"))

                    vendor_query = "SELECT IFNULL(TRIM(vendor_name), '') AS 'vendor_name', IFNULL(TRIM(vendor_code), '') AS 'vendor_code', IFNULL(TRIM(Location), '') AS 'Location', IFNULL(TRIM(address), '') AS 'address', IFNULL(TRIM(gst_number), '') AS 'gst_number', IFNULL(TRIM(email_id), '') AS 'email_id' FROM po_process.vendor_master WHERE is_active = 1;"
                    vendor_query_output = json.loads(execute_sql_query(vendor_query, object_type="table"))

                    approver_query = "SELECT user_name, mail_id, department FROM po_process.mail_credentials WHERE is_active = 1;"
                    approver_query_output = json.loads(execute_sql_query(approver_query, object_type="table"))

                    budget_allocation = BudgetAllocated.objects.filter(department=department)
                    for budget in budget_allocation:
                        allocated_budget = budget.budget_allocated

                    return JsonResponse({
                        "reporting_manager": reporting_manager,
                        # "budget_category": budget_category,
                        "allocated_budget": allocated_budget,
                        "prf_number": prf_number,
                        "location_list": query_output,
                        "vendor_list": vendor_query_output,
                        "approver_list": approver_query_output
                    })
                else:
                    return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
            else:
                return JsonResponse({"Status": "Error", "Message": "User Name Not Found!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting user details", exc_info=True)
        return JsonResponse({"Status": "Error"})


@csrf_exempt
def get_location_details(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)

            for k, v in data.items():
                if k == "location_name":
                    location_name = v

            if len(location_name) > 0:
                items = Location.objects.filter(location=location_name)

                for item in items:
                    address = item.address

                return JsonResponse({
                    "address": address
                })
            else:
                return JsonResponse({"Status": "Error", "Message": "Location Name Not Found!!!"})
        else:
            return JsonResponse({"Status": "Error", "Message": "POST Method Not Received!!!"})

    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Vendor Details", exc_info=True)
        return JsonResponse({"Status": "Error"})


@csrf_exempt
def get_vendor_name(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)

            for k, v in data.items():
                if k == "vendor_type":
                    vendor_type = v

            if vendor_type == "Existing":
                vendors = VendorMaster.objects.filter(is_active=1)
                vendor_names = []
                for vendor in vendors:
                    vendor_names.append(vendor.vendor_name)
                # print(vendor_names)

                return JsonResponse({"vendor_name": vendor_names})
        else:
            return JsonResponse({"Status": "Error", "Message": "POST Method Not Received!!!"})

    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Vendor Name", exc_info=True)
        return JsonResponse({"Status": "Error"})


@csrf_exempt
def get_vendor_details(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)

            for k, v in data.items():
                if k == "vendor_name":
                    vendor_name = v

            if len(vendor_name) > 0:
                vendors = VendorMaster.objects.filter(vendor_name=vendor_name)

                for vendor in vendors:
                    vendor_code = vendor.vendor_code
                    Location = vendor.Location
                    address = vendor.address
                    gst_number = vendor.gst_number
                    pan_number = vendor.pan_number

                return JsonResponse({
                    "vendor_code": vendor_code,
                    "Location": Location,
                    "address": address,
                    "gst_number": gst_number,
                    "pan_number": pan_number
                })
            else:
                return JsonResponse({"Status": "Error", "Message": "Vendor Name Not Found!!!"})
        else:
            return JsonResponse({"Status": "Error", "Message": "POST Method Not Received!!!"})

    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Vendor Details", exc_info=True)
        return JsonResponse({"Status": "Error"})


@csrf_exempt
def get_prf_details(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

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
                if k == "payment_term":
                    payment_term = v
                if k == "perceived_benefits":
                    benefits = v
                if k == "total_line_value":
                    total_line_value = v
                if k == "finalized_vendor":
                    finalized_vendor = v
                if k == "vendor_selection_reason":
                    vendor_selection_reason = v
                if k == "approver_name":
                    approver_name = v
                if k == "approver_mailid":
                    approver_mailid = v
                if k == "approver_department":
                    approver_department = v
                if k == "is_processed":
                    is_processed = v
                if k == "porequirementinfo":
                    porequirementinfo_list = v
                if k == "poquotation":
                    poquotation = v

            if is_processed == 0:
                prf_number_changed = prf_number
                po_status_changed = "INCOMPLETE"

            if is_processed == 1:
                prf_number_new = prf_number.split("-", 1)
                prf_number_changed = prf_number_new[0]
                po_status_changed = "SENT TO DEPARTMENT HEAD"

            # print(prf_number_changed)
            # print(prf_number_new)

            reqirement_details = PurchaseRequirement(
                tenant_id=tenant_id,
                group_id=group_id,
                entity_id=entity_id,
                module_id=module_id,
                prf_number=prf_number_changed,
                user_name=user_name,
                location=location,
                requirement_date=requirement_date,
                reporting_manager=reporting_manager,
                department=department,
                budget_allocated=budget_allocated,
                is_budgeted=is_budgeted,
                purpose=purpose,
                purchase_catagory=purchase_catagory,
                purchase_type=purchase_type,
                date_of_delivery_expected=date_of_delivery_expected,
                delivery_address=delivery_address,
                payment_term=payment_term,
                benefits=benefits,
                total_line_value=total_line_value,
                finalized_vendor=finalized_vendor,
                vendor_selection_reason=vendor_selection_reason,
                approver_name=approver_name,
                approver_mailid=approver_mailid,
                approver_department=approver_department,
                is_processed=is_processed,
                po_status=po_status_changed,
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
                for k, v in value.items():
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
                    tenant_id=tenant_id,
                    group_id=group_id,
                    entity_id=entity_id,
                    module_id=module_id,
                    prf_number=prf_number_changed,
                    material_name=material_name,
                    budget_category=budget_category,
                    line_description=line_description,
                    quantity=quantity,
                    unit_value=unit_value,
                    total_value=total_value,
                    is_active=1,
                    created_by=user_id,
                    created_date=timezone.now(),
                    modified_by=user_id,
                    modified_date=timezone.now(),
                    purchase_requirement_id=requirement_id,
                    uploaded_by=user_name
                )
                line_details.save()

            for values in poquotation:
                for k, v in values.items():
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
                    if k == "vendor_emailid":
                        mail_id = v
                    if k == "vendor_total_line_value":
                        vendor_total_line_value = v
                    if k == "quotationfile_name":
                        quotationfile_name = v
                    if k == "VendorFile_name":
                        VendorFile_name = v
                    if k == "quotation":
                        poquotationinfo = v

                quotation_details = QuotationDetails(
                    tenant_id=tenant_id,
                    group_id=group_id,
                    entity_id=entity_id,
                    module_id=module_id,
                    prf_number=prf_number_changed,
                    vendor_type=vendor_type,
                    vendor_name=vendor_name,
                    vendor_code=vendor_code,
                    address=address,
                    location=vendor_location,
                    gst_number=gst_number,
                    mail_id=mail_id,
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

                    quotation_line_details = QuotationLineDetails(
                        tenant_id=tenant_id,
                        group_id=group_id,
                        entity_id=entity_id,
                        module_id=module_id,
                        prf_number=prf_number_changed,
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

            return JsonResponse({"Status": "Success", "Message": "Data Uploaded Successfully!!!"})
        else:
            return JsonResponse({"Status": "Error", "Message": "POST Method Not Received!!!"})

    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting PRF details", exc_info=True)
        return JsonResponse({"status": "Error"})


@csrf_exempt
def get_file_upload(request, *args, **kwargs):
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
                                        is_processed = request.POST.get("is_processed")
                                        # print(prf_number)
                                        # print(is_processed)
                                        if is_processed == "0":
                                            prf_number_changed = prf_number

                                        elif is_processed == "1":
                                            prf_number_new = prf_number.split("-", 1)
                                            prf_number_changed = prf_number_new[0]
                                        # print(prf_number_changed)

                                        file_name = request.FILES["QuotationFile"].name
                                        vendor_name = request.POST.get("vendor_name")
                                        # print(vendor_name)
                                        file_name_extension = "." + file_name.split(".")[-1]
                                        file_name_without_extension = file_name.replace(file_name_extension, "")
                                        file_name_proper = file_name_without_extension.replace(".", "") + "_" + str(datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "_").replace(".", "_") + file_name_extension
                                        file_name_proper = file_name_proper.replace(" ", "_").replace("-","_").replace("'", "").replace("#", "_No_").replace("&", "_").replace("(", "_").replace(")", "_")
                                        file_type = file_name.split(".")[-1]

                                        details = PurchaseRequirement.objects.filter(prf_number=prf_number_changed)
                                        # print(details)
                                        for detail in details:
                                            requirement_id = detail.id
                                            # print(requirement_id)

                                        details = QuotationDetails.objects.filter(prf_number=prf_number_changed, vendor_name=vendor_name)
                                        for detail in details:
                                            quotation_id = detail.id

                                        # if file_type in ["PDF", "Pdf", "pdf"]:
                                        items = UniqueNumber.objects.filter(key='uploadFolder', expression='pdf')
                                        for item in items:
                                            file_path = item.value
                                            # print(file_path)

                                        file_upload_path_name_date = file_path + file_name_proper

                                        with open(file_upload_path_name_date, 'wb+') as destination:
                                            for chunk in request.FILES["QuotationFile"]:
                                                destination.write(chunk)

                                        upload_files = UploadFiles.objects.create(
                                            tenant_id=tenant_id,
                                            group_id=group_id,
                                            entity_id=entity_id,
                                            module_id=module_id,
                                            prf_number=prf_number_changed,
                                            category="Quotation",
                                            file_type=file_type,
                                            file_path=file_upload_path_name_date,
                                            is_active=1,
                                            created_by=user_id,
                                            created_date=timezone.now(),
                                            modified_by=user_id,
                                            modified_date=timezone.now(),
                                            uploaded_by=user_name,
                                            purchase_requirement_id=requirement_id,
                                            quotation_details_id=quotation_id
                                        )
                                        upload_files.save()

                                        values = QuotationDetails.objects.filter(prf_number=prf_number_changed, vendor_name=vendor_name)
                                        for value in values:
                                            value.quotationfile_name = file_name_proper
                                            value.save()

                                        return JsonResponse({"Status": "Success", "Message": "File Uploaded Successfully!!!"})
                                    else:
                                        return JsonResponse({"Status": "Error", "Message": "PRF Number Not Found!!!"})
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
        return JsonResponse({"Status": "Error"})

@csrf_exempt
def get_process_file_upload(request, *args, **kwargs):
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
                                        prf_number_new = prf_number.split("-", 1)
                                        prf_number_changed = prf_number_new[0]
                                        # print(prf_number_changed)

                                        file_name = request.FILES["QuotationFile"].name
                                        vendor_name = request.POST.get("vendor_name")
                                        # print(vendor_name)
                                        file_name_extension = "." + file_name.split(".")[-1]
                                        file_name_without_extension = file_name.replace(file_name_extension, "")
                                        file_name_proper = file_name_without_extension.replace(".", "") + "_" + str(datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "_").replace(".", "_") + file_name_extension
                                        file_name_proper = file_name_proper.replace(" ", "_").replace("-","_").replace("'", "").replace("#", "_No_").replace("&", "_").replace("(", "_").replace(")", "_")
                                        file_type = file_name.split(".")[-1]

                                        details = PurchaseRequirement.objects.filter(prf_number=prf_number_changed)
                                        # print(details)
                                        for detail in details:
                                            requirement_id = detail.id
                                            # print(requirement_id)

                                        details = QuotationDetails.objects.filter(prf_number=prf_number_changed, vendor_name=vendor_name)
                                        for detail in details:
                                            quotation_id = detail.id

                                        # if file_type in ["PDF", "Pdf", "pdf"]:
                                        items = UniqueNumber.objects.filter(key='uploadFolder', expression='pdf')
                                        for item in items:
                                            file_path = item.value
                                            # print(file_path)

                                        file_upload_path_name_date = file_path + file_name_proper

                                        with open(file_upload_path_name_date, 'wb+') as destination:
                                            for chunk in request.FILES["QuotationFile"]:
                                                destination.write(chunk)

                                        upload_files = UploadFiles.objects.create(
                                            tenant_id=tenant_id,
                                            group_id=group_id,
                                            entity_id=entity_id,
                                            module_id=module_id,
                                            prf_number=prf_number_changed,
                                            category="Quotation",
                                            file_type=file_type,
                                            file_path=file_upload_path_name_date,
                                            is_active=1,
                                            created_by=user_id,
                                            created_date=timezone.now(),
                                            modified_by=user_id,
                                            modified_date=timezone.now(),
                                            uploaded_by=user_name,
                                            purchase_requirement_id=requirement_id,
                                            quotation_details_id=quotation_id
                                        )
                                        upload_files.save()

                                        values = QuotationDetails.objects.filter(prf_number=prf_number_changed, vendor_name=vendor_name)
                                        for value in values:
                                            value.quotationfile_name = file_name_proper
                                            value.save()

                                        return JsonResponse({"Status": "Success", "Message": "File Uploaded Successfully!!!"})
                                    else:
                                        return JsonResponse({"Status": "Error", "Message": "PRF Number Not Found!!!"})
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
        return JsonResponse({"Status": "Error"})


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
                if k == "department":
                    department = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if department is not None:
                                    query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name', IFNULL(CASE WHEN po_status = 'HOLD BY DEPARTMENT HEAD' OR po_status = 'APPROVED BY DEPT, WAITING FOR VENDOR DOC' OR po_status = 'REJECTED BY DEPARTMENT HEAD' OR po_status = 'SENT TO P2P TEAM' THEN dept_head_approved_comments WHEN po_status = 'SENT TO FINANCE' OR po_status = 'HOLD BY P2P TEAM' OR po_status = 'REJECTED BY P2P TEAM' THEN p2p_approved_comments WHEN po_status = 'APPROVED BY FINANCE' OR po_status = 'HOLD BY FINANCE' OR po_status = 'REJECTED BY FINANCE' THEN finance_approved_comments END, '') AS 'Comments' FROM po_process.purchase_requirement WHERE created_by = '{user_id}' AND department = '{department}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_query = query.replace("{user_id}", str(user_id)).replace("{department}",str(department)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    return JsonResponse({"Status": "Success", "data": query_output["data"]})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Department Not Found!!!"})
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
        logger.error("Error in Getting User PRF List", exc_info=True)
        return JsonResponse({"Status": "Error"})


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

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:
                                    query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%Y-%m-%d'), '') AS 'requirement_date', IFNULL(TRIM(delivery_address), '') AS 'delivery_address', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(payment_term), '') AS 'payment_term', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status', is_processed AS 'is_processed', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE created_by = '{user_id}' AND id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_query = query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    line_query = "SELECT id AS poreqinfo_id, IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(budget_category), '') AS 'budget_category', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_line_query = line_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    line_query_output = json.loads(execute_sql_query(final_line_query, object_type="table"))
                                    quotation_query = "SELECT id AS pobudget_id, IFNULL(TRIM(vendor_type), '') AS 'vendor_type', IFNULL(TRIM(vendor_name), '') AS 'vendor_name', IFNULL(TRIM(vendor_code), '') AS 'vendor_code', IFNULL(TRIM(address), '') AS 'vendor_address', IFNULL(TRIM(location), '') AS 'vendor_location', IFNULL(TRIM(gst_number), '') AS 'gst_number', IFNULL(TRIM(mail_id), '') AS 'vendor_emailid', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'vendor_total_line_value', IFNULL(TRIM(quotationfile_name), '') AS 'quotationfile_name', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.quotation_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_quotation_query = quotation_query.replace("{user_id}", str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}",str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_query_output = json.loads(execute_sql_query(final_quotation_query, object_type="table"))
                                    quotation_line_query = "SELECT quotation_details_id AS pobudget_id, id AS pobudgetinfo_id, IFNULL(TRIM(material_name), '') AS 'vendor_material_name', IFNULL(TRIM(line_description), '') AS 'vendor_line_description', IFNULL(TRIM(quantity), '') AS 'vendor_quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'vendor_unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'vendor_total_value' FROM po_process.quotation_line_details WHERE created_by = '{user_id}' AND purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_quotation_line_query = quotation_line_query.replace("{user_id}",str(user_id)).replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}",str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_line_query_output = json.loads(execute_sql_query(final_quotation_line_query, object_type="table"))

                                    for output in quotation_query_output["data"]:
                                        quotation = []
                                        for line in quotation_line_query_output["data"]:
                                            if output["pobudget_id"] == line["pobudget_id"]:
                                                quotation.append(line)
                                        output["quotation"] = quotation
                                    po_requirement = {
                                        "prf_list": query_output["data"],
                                        "requirement_info": line_query_output["data"],
                                        "poquotation": quotation_query_output["data"]
                                    }
                                    return JsonResponse({"Status": "Success", "po_requirement": po_requirement})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Department Not Found!!!"})
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
        logger.error("Error in Getting PRF Form fields", exc_info=True)
        return JsonResponse({"Status": "Error"})


@csrf_exempt
def get_edit_prf_form_details(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

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
                if k == "vendor_selection_reason":
                    vendor_selection_reason = v
                if k == "approver_name":
                    approver_name = v
                if k == "approver_mailid":
                    approver_mailid = v
                if k == "approver_department":
                    approver_department = v
                if k == "is_processed":
                    is_processed = v
                if k == "porequirementinfo":
                    porequirementinfo_list = v
                if k == "poquotation":
                    poquotation_list = v
                if k == "requirement_id":
                    requirement_id = v

            if is_processed == 0:
                prf_number_changed = prf_number
                po_status_changed = "INCOMPLETE"

            if is_processed == 1:
                prf_number_new = prf_number.split("-", 1)
                prf_number_changed = prf_number_new[0]
                po_status_changed = "SENT TO DEPARTMENT HEAD"
            # print(poquotation_list)

            values = UploadFiles.objects.filter(purchase_requirement=requirement_id)
            for value in values:
                value.prf_number = prf_number_changed
                value.save()

            prf_details = PurchaseRequirement.objects.filter(id=requirement_id, tenant_id=tenant_id, group_id=group_id, entity_id=entity_id, module_id=module_id)

            for details in prf_details:
                details.prf_number = prf_number_changed
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
                details.is_processed = is_processed
                details.po_status = po_status_changed
                details.vendor_selection_reason = vendor_selection_reason
                details.approver_name = approver_name
                details.approver_mailid = approver_mailid
                details.approver_department = approver_department
                details.save()

            for value in porequirementinfo_list:
                for k, v in value.items():
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

                if line_id != 0:
                    items = LineDetails.objects.filter(id=line_id, tenant_id=tenant_id, group_id=group_id, entity_id=entity_id, module_id=module_id)

                    for item in items:
                        item.prf_number = prf_number_changed
                        item.material_name = material_name
                        item.budget_category = budget_category
                        item.line_description = line_description
                        item.quantity = quantity
                        item.unit_value = unit_value
                        item.total_value = total_value
                        item.save()

                elif line_id == 0:
                    line_details = LineDetails(
                        tenant_id=tenant_id,
                        group_id=group_id,
                        entity_id=entity_id,
                        module_id=module_id,
                        prf_number=prf_number_changed,
                        material_name=material_name,
                        budget_category=budget_category,
                        line_description=line_description,
                        quantity=quantity,
                        unit_value=unit_value,
                        total_value=total_value,
                        is_active=1,
                        created_by=user_id,
                        created_date=timezone.now(),
                        modified_by=user_id,
                        modified_date=timezone.now(),
                        purchase_requirement_id=requirement_id,
                        uploaded_by=user_name
                    )
                    line_details.save()

            for values in poquotation_list:
                for k, v in values.items():
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
                    if k == "vendor_emailid":
                        mail_id = v
                    if k == "vendor_total_line_value":
                        vendor_total_line_value = v
                    if k == "quotationfile_name":
                        quotationfile_name = v
                    if k == "VendorFile_name":
                        VendorFile_name = v
                    if k == "pobudget_id":
                        quotation_id = v
                    if k == "quotation":
                        poquotationinfo_list = v
                # print(quotation_id)
                # print(k,v)
                if quotation_id != 0:
                    quotations = QuotationDetails.objects.filter(id=quotation_id, tenant_id=tenant_id, group_id=group_id, entity_id=entity_id, module_id=module_id)

                    for quotation in quotations:
                        quotation.prf_number = prf_number_changed
                        quotation.vendor_type = vendor_type
                        quotation.vendor_name = vendor_name
                        quotation.vendor_code = vendor_code
                        quotation.address = address
                        quotation.vendor_location = vendor_location
                        quotation.gst_number = gst_number
                        quotation.mail_id = mail_id
                        quotation.total_line_value = vendor_total_line_value
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

                        if quotation_line_id != 0:
                            values = QuotationLineDetails.objects.filter(id=quotation_line_id, tenant_id=tenant_id, group_id=group_id, entity_id=entity_id, module_id=module_id)
                            # print(values)

                            for value in values:
                                value.prf_number = prf_number_changed
                                value.vendor_material_name = vendor_material_name
                                value.vendor_line_description = vendor_line_description
                                value.vendor_quantity = vendor_quantity
                                value.vendor_unit_value = vendor_unit_value
                                value.vendor_total_value = vendor_total_value
                                value.save()

                        elif quotation_line_id == 0:

                            quotation_line_details = QuotationLineDetails(
                                tenant_id=tenant_id,
                                group_id=group_id,
                                entity_id=entity_id,
                                module_id=module_id,
                                prf_number=prf_number_changed,
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

                elif quotation_id == 0:
                    for values in poquotation_list:
                        for k, v in values.items():
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
                            if k == "vendor_emailid":
                                mail_id = v
                            if k == "vendor_total_line_value":
                                vendor_total_line_value = v
                            if k == "quotationfile_name":
                                quotationfile_name = v
                            if k == "VendorFile_name":
                                VendorFile_name = v
                            if k == "quotation":
                                poquotationinfo = v
                    quotation_details = QuotationDetails(
                        tenant_id=tenant_id,
                        group_id=group_id,
                        entity_id=entity_id,
                        module_id=module_id,
                        prf_number=prf_number_changed,
                        vendor_type=vendor_type,
                        vendor_name=vendor_name,
                        vendor_code=vendor_code,
                        address=address,
                        location=vendor_location,
                        gst_number=gst_number,
                        mail_id=mail_id,
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


                    details = QuotationDetails.objects.filter(prf_number=prf_number_changed)
                    # print(details)
                    for detail in details:
                        vendor_id = detail.id
                        # print(vendor_id)

                    for value in poquotationinfo:
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
                            # print(vendor_total_value)

                        quotation_line_details = QuotationLineDetails(
                            tenant_id=tenant_id,
                            group_id=group_id,
                            entity_id=entity_id,
                            module_id=module_id,
                            prf_number=prf_number_changed,
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
                            quotation_details_id=vendor_id,
                            uploaded_by=user_name
                        )
                        quotation_line_details.save()

            return JsonResponse({"Status": "Success", "Message": "Data Uploaded Successfully!!!"})

        else:
            return JsonResponse({"Status": "Error", "Message": "POST Method Not Received!!!"})
    except Exception as e:
        logger.error(str(e))
        logger.error("Error in Getting Edit PRF Form Details", exc_info=True)
        return JsonResponse({"Status": "Error"})

# For vendor file upload
@csrf_exempt
def get_vendor_file_upload(request, *args, **kwargs):
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
                                        # vendor_name = request.POST.get("vendor_name")
                                        file_name = request.FILES["VendorFile"].name
                                        file_name_extension = "." + file_name.split(".")[-1]
                                        file_name_without_extension = file_name.replace(file_name_extension, "")
                                        file_name_proper = file_name_without_extension.replace(".", "") + "_" + str(datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "_").replace(".", "_") + file_name_extension
                                        file_name_proper = file_name_proper.replace(" ", "_").replace("-", "_").replace("'", "").replace("#", "_No_").replace("&", "_").replace("(", "_").replace(")", "_")
                                        file_type = file_name.split(".")[-1]

                                        details = PurchaseRequirement.objects.filter(prf_number=prf_number)
                                        for detail in details:
                                            requirement_id = detail.id

                                        # details = QuotationDetails.objects.filter(prf_number=prf_number)
                                        # for detail in details:
                                        #     quotation_id = detail.id
                                        # print(quotation_id)

                                        # if file_type in ["PDF", "Pdf", "pdf"]:
                                        items = UniqueNumber.objects.filter(key='vendorUploadFolder', expression='pdf')
                                        for item in items:
                                            file_path = item.value

                                        file_upload_path_name_date = file_path + file_name_proper

                                        with open(file_upload_path_name_date, 'wb+') as destination:
                                            for chunk in request.FILES["VendorFile"]:
                                                destination.write(chunk)

                                        vendor_files = VendorFiles.objects.create(
                                            tenant_id=tenant_id,
                                            group_id=group_id,
                                            entity_id=entity_id,
                                            module_id=module_id,
                                            prf_number=prf_number,
                                            category="Vendor",
                                            file_type=file_type,
                                            file_path=file_upload_path_name_date,
                                            is_active=1,
                                            created_by=user_id,
                                            created_date=timezone.now(),
                                            modified_by=user_id,
                                            modified_date=timezone.now(),
                                            uploaded_by=user_name,
                                            purchase_requirement_id=requirement_id
                                        )
                                        vendor_files.save()

                                        values = PurchaseRequirement.objects.filter(prf_number=prf_number)
                                        for value in values:
                                            name = value.VendorFile_name

                                        if name is None:
                                            values = PurchaseRequirement.objects.filter(prf_number=prf_number)
                                            for value in values:
                                                value.is_dept_head_approved = 1
                                                value.is_processed = 1
                                                value.po_status = "SENT TO P2P TEAM"
                                                value.dept_head_approved_date = timezone.now()
                                                value.VendorFile_name = file_name_proper
                                                value.save()
                                        elif name is not None:
                                            values = PurchaseRequirement.objects.filter(prf_number=prf_number)
                                            for value in values:
                                                value.is_dept_head_approved = 1
                                                value.is_processed = 1
                                                value.po_status = "SENT TO P2P TEAM"
                                                value.dept_head_approved_date = timezone.now()
                                                value.VendorFile_name = name + "," + " " + file_name_proper
                                                value.save()

                                        return JsonResponse(
                                            {"Status": "Success", "Message": "Vendor Documents Uploaded Successfully!!!"})
                                    else:
                                        return JsonResponse({"Status": "Error", "Message": "PRF Number Not Found!!!"})
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
        logger.error("Error in Getting Vendor File Upload", exc_info=True)
        return JsonResponse({"Status": "Error"})


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
                if k == "department":
                    department = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if department is not None:
                                    query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE is_processed = 1 AND approver_department = '{department}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_dept_head_approved = 0 AND is_active = 1;"
                                    final_query = query.replace("{department}", str(department)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    approved_query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE is_processed = 1 AND approver_department = '{department}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_dept_head_approved = 1 AND is_active = 1;"
                                    final_approved_query = approved_query.replace("{department}", str(department)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}",str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    final_approved_query_output = json.loads(execute_sql_query(final_approved_query, object_type="table"))
                                    return JsonResponse({"Status": "Success", "data": query_output["data"], "approved_list": final_approved_query_output["data"]})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Department Not Found!!!"})
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
        logger.error("Error in Getting Department Head PRF List", exc_info=True)
        return JsonResponse({"Status": "Error"})


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

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:
                                    query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%Y-%m-%d'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(payment_term), '') AS 'payment_term', IFNULL(TRIM(delivery_address), '') AS 'delivery_address', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status', is_processed AS 'is_processed', is_dept_head_approved, IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE is_processed = 1 AND id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_query = query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    line_query = "SELECT id AS poreqinfo_id, IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(budget_category), '') AS 'budget_category', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.line_details WHERE purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_line_query = line_query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    line_query_output = json.loads(execute_sql_query(final_line_query, object_type="table"))
                                    quotation_query = "SELECT id AS pobudget_id, IFNULL(TRIM(vendor_type), '') AS 'vendor_type', IFNULL(TRIM(vendor_name), '') AS 'vendor_name', IFNULL(TRIM(vendor_code), '') AS 'vendor_code', IFNULL(TRIM(address), '') AS 'vendor_address', IFNULL(TRIM(location), '') AS 'vendor_location', IFNULL(TRIM(gst_number), '') AS 'gst_number', IFNULL(TRIM(mail_id), '') AS 'vendor_emailid', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'vendor_total_line_value', quotationfile_name FROM po_process.quotation_details WHERE purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_quotation_query = quotation_query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}",str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_query_output = json.loads(execute_sql_query(final_quotation_query, object_type="table"))
                                    quotation_line_query = "SELECT quotation_details_id AS pobudget_id, id AS pobudgetinfo_id, IFNULL(TRIM(material_name), '') AS 'vendor_material_name', IFNULL(TRIM(line_description), '') AS 'vendor_line_description', IFNULL(TRIM(quantity), '') AS 'vendor_quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'vendor_unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'vendor_total_value' FROM po_process.quotation_line_details WHERE purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_quotation_line_query = quotation_line_query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_line_query_output = json.loads(execute_sql_query(final_quotation_line_query, object_type="table"))

                                    for output in quotation_query_output["data"]:
                                        quotation = []
                                        for line in quotation_line_query_output["data"]:
                                            if output["pobudget_id"] == line["pobudget_id"]:
                                                quotation.append(line)
                                        output["quotation"] = quotation
                                    # print(quotation_query_output["data"])
                                    po_requirement = {
                                        "prf_list": query_output["data"],
                                        "requirement_info": line_query_output["data"],
                                        "poquotation": quotation_query_output["data"]
                                    }
                                    return JsonResponse({"Status": "Success", "po_requirement": po_requirement})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Department Not Found!!!"})
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
        logger.error("Error in Getting Department Head PRF Form fields", exc_info=True)
        return JsonResponse({"Status": "Error"})


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
                if k == "finalized_vendor":
                    finalized_vendor = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:

                                    values = QuotationDetails.objects.filter(vendor_name=finalized_vendor, purchase_requirement_id=requirement_id)
                                    for value in values:
                                        vendor_type = value.vendor_type
                                        # print(vendor_type)

                                    orders = PurchaseRequirement.objects.filter(id=requirement_id, tenant_id=tenant_id,group_id=group_id, entity_id=entity_id, module_id=module_id)

                                    if is_dept_head_approved == 1:
                                        if vendor_type == "Existing":
                                            for order in orders:
                                                order.is_dept_head_approved = is_dept_head_approved
                                                order.po_status = "SENT TO P2P TEAM"
                                                order.dept_head_approved_date = timezone.now()
                                                order.dept_head_approved_comments = remarks
                                                order.save()

                                        elif vendor_type == "New":
                                            for order in orders:
                                                order.is_dept_head_approved = 4
                                                order.is_processed = 2
                                                order.po_status = "APPROVED BY DEPT, WAITING FOR VENDOR DOC"
                                                order.save()

                                    elif is_dept_head_approved == 2:
                                        for order in orders:
                                            order.is_dept_head_approved = is_dept_head_approved
                                            order.po_status = "HOLD BY DEPARTMENT HEAD"
                                            order.is_processed = 0
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
        return JsonResponse({"Status": "Error"})


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

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_p2p_approved = 0 AND is_active = 1;"
                                final_query = query.replace("{tenants_id}", str(tenant_id)).replace("{groups_id}",str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                approved_query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_p2p_approved = 1 AND is_active = 1;"
                                final_approved_query = approved_query.replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                final_approved_query_output = json.loads(execute_sql_query(final_approved_query, object_type="table"))
                                return JsonResponse({"Status": "Success", "data": query_output["data"], "approved_list": final_approved_query_output["data"]})
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
        logger.error("Error in Getting P2P Team PRF List", exc_info=True)
        return JsonResponse({"Status": "Error"})


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

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:
                                    query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%Y-%m-%d'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(payment_term), '') AS 'payment_term', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(delivery_address), '') AS 'delivery_address', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(po_status), '') AS 'po_status', is_processed, is_dept_head_approved, is_p2p_approved, IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_query = query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    line_query = "SELECT id AS poreqinfo_id, IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(budget_category), '') AS 'budget_category', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.line_details WHERE purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_line_query = line_query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    line_query_output = json.loads(execute_sql_query(final_line_query, object_type="table"))
                                    quotation_query = "SELECT id AS pobudget_id, IFNULL(TRIM(vendor_type), '') AS 'vendor_type', IFNULL(TRIM(vendor_name), '') AS 'vendor_name', IFNULL(TRIM(vendor_code), '') AS 'vendor_code', IFNULL(TRIM(address), '') AS 'vendor_address', IFNULL(TRIM(location), '') AS 'vendor_location', IFNULL(TRIM(gst_number), '') AS 'gst_number', IFNULL(TRIM(mail_id), '') AS 'vendor_emailid', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'vendor_total_line_value', quotationfile_name FROM po_process.quotation_details WHERE purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_quotation_query = quotation_query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_query_output = json.loads(execute_sql_query(final_quotation_query, object_type="table"))
                                    quotation_line_query = "SELECT quotation_details_id AS pobudget_id, id AS pobudgetinfo_id, IFNULL(TRIM(material_name), '') AS 'vendor_material_name', IFNULL(TRIM(line_description), '') AS 'vendor_line_description', IFNULL(TRIM(quantity), '') AS 'vendor_quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'vendor_unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'vendor_total_value' FROM po_process.quotation_line_details WHERE purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_quotation_line_query = quotation_line_query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_line_query_output = json.loads(execute_sql_query(final_quotation_line_query, object_type="table"))
                                    for output in quotation_query_output["data"]:
                                        quotation = []
                                        for line in quotation_line_query_output["data"]:
                                            if output["pobudget_id"] == line["pobudget_id"]:
                                                quotation.append(line)
                                        output["quotation"] = quotation
                                    po_requirement = {
                                        "prf_list": query_output["data"],
                                        "requirement_info": line_query_output["data"],
                                        "poquotation": quotation_query_output["data"]
                                    }
                                    return JsonResponse({"Status": "Success", "po_requirement": po_requirement})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Department Not Found!!!"})
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
        logger.error("Error in Getting P2P Team PRF Form fields", exc_info=True)
        return JsonResponse({"Status": "Error"})


# For p2p team po file upload
@csrf_exempt
def get_po_file_upload(request, *args, **kwargs):
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
                                        file_name = request.FILES["POFile"].name
                                        file_name_extension = "." + file_name.split(".")[-1]
                                        file_name_without_extension = file_name.replace(file_name_extension, "")
                                        file_name_proper = file_name_without_extension.replace(".", "") + "_" + str(datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "_").replace(".", "_") + file_name_extension
                                        file_name_proper = file_name_proper.replace(" ", "_").replace("-", "_").replace("'", "").replace("#", "_No_").replace("&", "_").replace("(", "_").replace(")", "_")
                                        file_type = file_name.split(".")[-1]

                                        details = PurchaseRequirement.objects.filter(prf_number=prf_number)
                                        for detail in details:
                                            requirement_id = detail.id

                                        # details = QuotationDetails.objects.filter(prf_number=prf_number)
                                        # for detail in details:
                                        #     quotation_id = detail.id

                                        if file_type in ["PDF", "Pdf", "pdf"]:
                                            items = UniqueNumber.objects.filter(key='poUploadFolder', expression='pdf')
                                            for item in items:
                                                file_path = item.value

                                            file_upload_path_name_date = file_path + file_name_proper

                                            with open(file_upload_path_name_date, 'wb+') as destination:
                                                for chunk in request.FILES["POFile"]:
                                                    destination.write(chunk)

                                            po_files = POFiles.objects.create(
                                                tenant_id=tenant_id,
                                                group_id=group_id,
                                                entity_id=entity_id,
                                                module_id=module_id,
                                                prf_number=prf_number,
                                                category="PO",
                                                file_type=file_type,
                                                file_path=file_upload_path_name_date,
                                                is_active=1,
                                                created_by=user_id,
                                                created_date=timezone.now(),
                                                modified_by=user_id,
                                                modified_date=timezone.now(),
                                                uploaded_by=user_name,
                                                purchase_requirement_id=requirement_id
                                            )
                                            po_files.save()

                                        values = PurchaseRequirement.objects.filter(prf_number=prf_number)
                                        for value in values:
                                            value.is_po_issued = 1
                                            value.po_issued_date = timezone.now()
                                            value.po_file_name = file_name_proper
                                            value.save()

                                        return JsonResponse({"Status": "Success", "Message": "File Uploaded Successfully!!!"})
                                    else:
                                        return JsonResponse({"Status": "Error", "Message": "PRF Number Not Found!!!"})
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
        return JsonResponse({"Status": "Error"})


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
                if k == "finance_approver":
                    finance_approver = v
                if k == "prf_number":
                    prf_number = v

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
                                            order.po_status = "SENT TO FINANCE"
                                            order.p2p_approved_date = timezone.now()
                                            order.p2p_approved_comments = remarks
                                            order.finance_approver = finance_approver
                                            order.save()
                                            details = MailCredentials.objects.filter(user_name=finance_approver)
                                            for detail in details:
                                                user_name = detail.user_name
                                                approver_mail = detail.mail_id
                                                password1 = detail.password
                                                link = "http://154.61.75.57:4201"
                                                subject = "PRF For Approval"
                                                from_mail_id = "rajichawla0925@gmail.com"
                                                password = "Ponn1234@raj"
                                                body = "Dear" + " " + user_name + "," + """\n""" + """\t\t""" + prf_number + """ """ + """is generated for your approval. Click the below link to login and approve the PRF.""" + """\n\n""" + """Application Link - """ + link + """\n""" + """Mail Id - """ + approver_mail + """\n""" + """Password - """ + password1 + """\n\n\n""" + """Thanks and Regards""" + """\n""" + """Teamlease Services Limited"""
                                                # print(body)
                                                if (resend_approved_mail(approver_mail, body, subject, from_mail_id, password)):

                                                    logger.info("Approval Email send to the Finance Head")
                                                    # print("Success")
                                                    logger.info(approver_mail)
                                                else:
                                                    logger.error("Approval Email Not sent to the Finance Head")


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
        return JsonResponse({"Status": "Error"})


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

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                values = MailCredentials.objects.filter(user_id=user_id)
                                for value in values:
                                    user_name = value.user_name
                                # print(user_name)
                                query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(po_status), '') AS 'po_status', IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND is_p2p_approved = 1 AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND finance_approver = '{finance_approver}' AND is_finance_approved = 0 AND is_active = 1;"
                                final_query = query.replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id)).replace("{finance_approver}", user_name)
                                # print(final_query)
                                query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                approved_query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(po_status), '') AS 'po_status', IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND is_p2p_approved = 1 AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_finance_approved = 1 AND is_active = 1;"
                                final_approved_query = approved_query.replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                final_approved_query_output = json.loads(execute_sql_query(final_approved_query, object_type="table"))
                                return JsonResponse({"Status": "Success", "data": query_output["data"], "approved_list" : final_approved_query_output["data"]})
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
        logger.error("Error in Getting Finance PRF List", exc_info=True)
        return JsonResponse({"Status": "Error"})


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

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            if len(str(user_id)) > 0:
                                if len(str(requirement_id)) > 0:
                                    query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%Y-%m-%d'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(payment_term), '') AS 'payment_term', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(TRIM(date_of_delivery_expected), '') AS 'date_of_delivery_expected', IFNULL(TRIM(delivery_address), '') AS 'delivery_address', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(po_status), '') AS 'po_status', is_processed, is_dept_head_approved, is_p2p_approved, is_finance_approved, IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE is_processed = 1 AND is_dept_head_approved = 1 AND is_p2p_approved = 1 AND id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_query = query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                                    line_query = "SELECT id AS poreqinfo_id, IFNULL(TRIM(material_name), '') AS 'material_name', IFNULL(TRIM(budget_category), '') AS 'budget_category', IFNULL(TRIM(line_description), '') AS 'line_description', IFNULL(TRIM(quantity), '') AS 'quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'total_value' FROM po_process.line_details WHERE purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_line_query = line_query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    line_query_output = json.loads(execute_sql_query(final_line_query, object_type="table"))
                                    quotation_query = "SELECT id AS pobudget_id, IFNULL(TRIM(vendor_type), '') AS 'vendor_type', IFNULL(TRIM(vendor_name), '') AS 'vendor_name', IFNULL(TRIM(vendor_code), '') AS 'vendor_code', IFNULL(TRIM(address), '') AS 'vendor_address', IFNULL(TRIM(location), '') AS 'vendor_location', IFNULL(TRIM(gst_number), '') AS 'gst_number', IFNULL(TRIM(mail_id), '') AS 'vendor_emailid', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'vendor_total_line_value', quotationfile_name FROM po_process.quotation_details WHERE purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_quotation_query = quotation_query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}",str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_query_output = json.loads(execute_sql_query(final_quotation_query, object_type="table"))
                                    quotation_line_query = "SELECT quotation_details_id AS pobudget_id, id AS pobudgetinfo_id, IFNULL(TRIM(material_name), '') AS 'vendor_material_name', IFNULL(TRIM(line_description), '') AS 'vendor_line_description', IFNULL(TRIM(quantity), '') AS 'vendor_quantity', IFNULL(CONVERT(unit_value, CHAR), '0.00') AS 'vendor_unit_value', IFNULL(CONVERT(total_value, CHAR), '0.00') AS 'vendor_total_value' FROM po_process.quotation_line_details WHERE purchase_requirement_id = '{requirement_id}' AND tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                                    final_quotation_line_query = quotation_line_query.replace("{requirement_id}", str(requirement_id)).replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                                    quotation_line_query_output = json.loads(execute_sql_query(final_quotation_line_query, object_type="table"))
                                    for output in quotation_query_output["data"]:
                                        quotation = []
                                        for line in quotation_line_query_output["data"]:
                                            if output["pobudget_id"] == line["pobudget_id"]:
                                                quotation.append(line)
                                        output["quotation"] = quotation
                                    po_requirement = {
                                        "prf_list": query_output["data"],
                                        "requirement_info": line_query_output["data"],
                                        "poquotation": quotation_query_output["data"]
                                    }
                                    return JsonResponse({"Status": "Success", "po_requirement": po_requirement})
                                else:
                                    return JsonResponse({"Status": "Error", "Message": "Department Not Found!!!"})
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
        logger.error("Error in Getting Finance PRF Form fields", exc_info=True)
        return JsonResponse({"Status": "Error"})


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
                                            order.is_processed = 0
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
        return JsonResponse({"Status": "Error"})

# To get PRF list
@csrf_exempt
def get_admin_list(request, *args, **kwargs):
    try:
        if request.method == "POST":
            body = request.body.decode('utf-8')
            data = json.loads(body)
            # print(data)

            tenant_id = ''
            group_id = ''
            entity_id = ''
            module_id = ''
            # user_id = ''

            for k, v in data.items():
                if k == "tenant_id":
                    tenant_id = v
                if k == "group_id":
                    group_id = v
                if k == "entity_id":
                    entity_id = v
                if k == "module_id":
                    module_id = v

            if len(str(tenant_id)) > 0:
                if len(str(group_id)) > 0:
                    if len(str(entity_id)) > 0:
                        if len(str(module_id)) > 0:
                            # if len(str(user_id)) > 0:
                            #     if department is not None:
                            query = "SELECT id AS requirement_id, IFNULL(TRIM(prf_number), '') AS 'prf_number', IFNULL(TRIM(location), '') AS 'location', IFNULL(DATE_FORMAT(requirement_date, '%d-%m-%Y'), '') AS 'requirement_date', IFNULL(TRIM(reporting_manager), '') AS 'reporting_manager', IFNULL(TRIM(department), '') AS 'department', IFNULL(TRIM(budget_allocated), '') AS 'budget_allocated', IFNULL(TRIM(is_budgeted), '') AS 'is_budgeted', IFNULL(TRIM(purpose), '') AS 'purpose', IFNULL(TRIM(purchase_catagory), '') AS 'purchase_catagory', IFNULL(TRIM(purchase_type), '') AS 'purchase_type', IFNULL(DATE_FORMAT(date_of_delivery_expected, '%d-%m-%Y'), '') AS 'date_of_delivery_expected', IFNULL(TRIM(benefits), '') AS 'perceived_benefits', IFNULL(CONVERT(total_line_value, CHAR), '0.00') AS 'total_line_value', IFNULL(TRIM(finalized_vendor), '') AS 'finalized_vendor', IFNULL(TRIM(po_status), '') AS 'po_status', IFNULL(TRIM(po_file_name), '') AS 'po_file_name', IFNULL(TRIM(approver_name),'') AS 'approver_name', IFNULL(TRIM(approver_department),'') AS 'approver_department', IFNULL(TRIM(approver_mailid),'') AS 'approver_mailid', IFNULL(TRIM(vendor_selection_reason),'') AS 'vendor_selection_reason', IFNULL(TRIM(VendorFile_name), '') AS 'VendorFile_name' FROM po_process.purchase_requirement WHERE tenant_id = '{tenants_id}' AND group_id = '{groups_id}' AND entity_id = '{entities_id}' AND module_id = '{module_id}' AND is_active = 1;"
                            final_query = query.replace("{tenants_id}", str(tenant_id)).replace("{groups_id}", str(group_id)).replace("{entities_id}", str(entity_id)).replace("{module_id}", str(module_id))
                            query_output = json.loads(execute_sql_query(final_query, object_type="table"))
                            return JsonResponse({"Status": "Success", "data": query_output["data"]})
                            #     else:
                            #         return JsonResponse({"Status": "Error", "Message": "Department Not Found!!!"})
                            # else:
                            #     return JsonResponse({"Status": "Error", "Message": "User Id Not Found!!!"})
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
        logger.error("Error in Getting User PRF List", exc_info=True)
        return JsonResponse({"Status": "Error"})