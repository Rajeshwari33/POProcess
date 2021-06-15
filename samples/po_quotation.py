quotation_query_output = [
    {
        "pobudget_id": "17",
        "vendor_type": "New1",
        "vendor_name": "Teamlease",
        "vendor_code": "V02314",
        "address": "xxx,zzzz",
        "location": "Chennai",
        "gst_number": "AD739872387Z",
        "vendor_emailid": "",
        "total_line_value": "63789.00"
    },
    {
        "pobudget_id": "18",
        "vendor_type": "New",
        "vendor_name": "Teamlease",
        "vendor_code": "V02314",
        "address": "xxx,yyyy,zzzz",
        "location": "Chennai",
        "gst_number": "AD739872387Z",
        "vendor_emailid": "",
        "total_line_value": "63789.00"
    }
]

quottation_query_line_output = [
    {
        "pobudget_id": "17",
        "pobudgetinfo_id": "28",
        "material_name": "Material",
        "line_description": "good, bad",
        "quantity": "2",
        "unit_value": "200.00",
        "total_value": "400.00"
    },
    {
        "pobudget_id": "17",
        "pobudgetinfo_id": "29",
        "material_name": "Material",
        "line_description": "good, bad",
        "quantity": "2",
        "unit_value": "200.00",
        "total_value": "400.00"
    },
    {
        "pobudget_id": "17",
        "pobudgetinfo_id": "30",
        "material_name": "Material",
        "line_description": "good, bad",
        "quantity": "2",
        "unit_value": "200.00",
        "total_value": "400.00"
    },
    {
        "pobudget_id": "18",
        "pobudgetinfo_id": "31",
        "material_name": "Material",
        "line_description": "good, bad",
        "quantity": "2",
        "unit_value": "200.00",
        "total_value": "400.00"
    },
    {
        "pobudget_id": "18",
        "pobudgetinfo_id": "32",
        "material_name": "Material",
        "line_description": "good, bad",
        "quantity": "2",
        "unit_value": "200.00",
        "total_value": "400.00"
    },
    {
        "pobudget_id": "18",
        "pobudgetinfo_id": "33",
        "material_name": "Material",
        "line_description": "good, bad",
        "quantity": "2",
        "unit_value": "200.00",
        "total_value": "400.00"
    }
]



for output in quotation_query_output:
    quotation = []
    for line in quottation_query_line_output:
        if output["pobudget_id"] == line["pobudget_id"]:
            quotation.append(line)
    output["quotation"] = quotation

print(quotation_query_output)