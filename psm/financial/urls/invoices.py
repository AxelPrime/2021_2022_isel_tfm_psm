from ..views.api.invoices import *
from django.urls import path


urlpatterns = [
    # GET
    path("monthly-invoices/details/", monthly_invoice_details_api),
    path("monthly-invoices/download/", download_invoice_file_api),
    path("monthly-invoices/superuser-verify/", superuser_invoices_to_create_api),
    path("yearly-invoices/download/", download_yearly_invoice_api),

    # POST
    path("monthly-invoices/create/", create_monthly_invoice_api),
    path("monthly-invoices/finalize/", finalize_monthly_invoice_api),
    path("monthly-invoices/evaluate/", evaluate_monthly_invoice_api),

    # PUT
]