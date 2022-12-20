from django.urls import path
from ..views.api.datatables import *


urlpatterns = [
    path('yearly-invoice/details/', get_yearly_invoice_data_api)
]
