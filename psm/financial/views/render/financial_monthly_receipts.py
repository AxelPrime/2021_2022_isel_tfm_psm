from datetime import date, timedelta

from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from financial.models import MonthlyInvoice
from user_management.models import CustomUser
from utils.user_context import get_user_context
import calendar
from dateutil.relativedelta import relativedelta
from financial.utils.check_can_create_invoice import check_can_create_invoice

ALLOWED_USERS = [
    'financial',
    'superuser',
]

TYPOLOGIES = [
    'I', 'II', 'III'
]


@sync_to_async()
def financial_monthly_receipt_list_page(request):
    if request.method == 'GET':
        user = request.user  # type: CustomUser
        if not user.is_authenticated or user.user_type not in ALLOWED_USERS:
            return redirect('/login/')

        invoices = [
            {
                'id': i.invoice_number,
                'typology': i.typology,
                'care_house': i.care_house.name,
                'start_date': i.start_date.strftime('%d/%m/%Y'),
                'end_date': i.end_date.strftime('%d/%m/%Y'),
                'total_patients': i.invoice_lines['total_patients'],
                'total_amount': i.invoice_lines['total_amount'],
                'status': i.get_status_display()
            }
            for i in MonthlyInvoice.objects.filter(
                status='awaits_payment'
            )
        ]

        # Obtain the next invoices.
        # next_invoices, cookies = check_can_create_invoice(TYPOLOGIES, user)

        context = {
            'invoices': invoices,
            # 'datatable_url': '/api/datatables/finances/receipts/',
            'user': get_user_context(user),
            # 'next_invoices': next_invoices
        }

        response = render(request, 'finances/html/financial_monthly_receipts.html', context=context)
        # for c in cookies:
        #     response.set_cookie(c['key'], c['value'])

        return response
    else:
        return redirect('/login/')
