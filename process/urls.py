from django.urls import path
from . import views

urlpatterns = [
    path('user_details/', views.get_user_details, name="user_details"),
    path('location_details/', views.get_location_details, name="location_details"),
    path('prf_form/', views.get_prf_details, name="prf_form"),
    path('vendor_name/', views.get_vendor_name, name="vendor_name"),
    path('vendor_details/', views.get_vendor_details, name="vendor_details"),
    path('quotation_file_upload/', views.get_file_upload, name="quotation_file_upload"),
    path('processed_quotation_file_upload/', views.get_process_file_upload, name="processed_quotation_file_upload"),
    path('user_prf_list/', views.get_user_prf_list, name="user_prf_list"),
    path('user_prf_input_fields/', views.get_prf_form_input_fields, name="user_prf_input_fields"),
    path('edit_prf_form/', views.get_edit_prf_form_details, name="edit_prf_form"),
    path('vendor_file_upload/', views.get_vendor_file_upload, name="vendor_file_upload"),
    path('dept_head_prf_list/', views.get_dept_head_prf_list, name="dept_head_prf_list"),
    path('dept_head_prf_input_fields/', views.get_dept_head_prf_form_input_fields, name="dept_head_prf_input_fields"),
    path('dept_head_functionality/', views.dept_head_functionality, name="dept_head_functionality"),
    path('p2p_team_prf_list/', views.get_p2p_team_prf_list, name="p2p_team_prf_list"),
    path('p2p_team_prf_input_fields/', views.get_p2p_team_prf_form_input_fields, name="p2p_team_prf_input_fields"),
    path('po_file_upload/', views.get_po_file_upload, name="po_file_upload"),
    path('p2p_team_functionality/', views.p2p_team_functionality, name="p2p_team_functionality"),
    path('finance_prf_list/', views.get_finance_prf_list, name="finance_prf_list"),
    path('finance_prf_input_fields/', views.get_finance_prf_form_input_fields, name="finance_prf_input_fields"),
    path('finance_functionality/', views.finance_functionality, name="finance_functionality"),
    path('admin_list/', views.get_admin_list, name="admin_list"),
]