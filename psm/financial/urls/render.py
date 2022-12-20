from django.urls import path
from ..views.render import *


urlpatterns = [
    # Care House
    path('care-house/finances/receipts/', receipt_list_page),
    path('care-house/finances/receipt-history/', receipt_history_page),

    # Financial Staff
    path('financial/finances/monthly-receipts/', financial_monthly_receipt_list_page),
    path('financial/finances/receipt-history/', financial_receipt_history_page),
    path('financial/finances/stats/typology/', typology_stats_page),
    path('financial/finances/stats/typology-ii/', typology_ii_stats_page),
    path('financial/finances/yearly-invoices/', yearly_invoices_page),

    # Super User
    path('superuser/care-house/finances/receipts/', superuser_monthly_receipt_list_page),
    path('superuser/financial/finances/monthly-receipts/', financial_monthly_receipt_list_page),
    path('superuser/financial/finances/receipt-history/', financial_receipt_history_page),
    path('superuser/financial/finances/stats/typology/', typology_stats_page),
    path('superuser/financial/finances/stats/typology-ii/', typology_ii_stats_page),
    path('superuser/financial/finances/yearly-invoices/', yearly_invoices_page),
    path('superuser/daily-values/', daily_values_page),
]