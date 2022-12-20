from datetime import date, timedelta

from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from entities.models import CareHouse
from financial.models import MonthlyInvoice
from user_management.models import CustomUser
from utils.user_context import get_user_context
import calendar
from dateutil.relativedelta import relativedelta
from financial.utils.check_can_create_invoice import check_can_create_invoice

ALLOWED_USERS = [
    'care_house_staff',
]

TYPOLOGIES = [
    'I', 'II', 'III'
]


@sync_to_async()
def receipt_list_page(request):
    if request.method == 'GET':
        user = request.user  # type: CustomUser
        if not user.is_authenticated or user.user_type not in ALLOWED_USERS:
            return redirect('/login/')

        # The active status.
        active_status = ['temp', 'awaits_payment']

        # Define the query.
        if user.user_type == 'care_house_staff':
            query = MonthlyInvoice.objects.filter(
                care_house=user.care_house,
                status__in=active_status
            )
        else:
            query = MonthlyInvoice.objects.filter(
                status__in=active_status
            )

        invoices = [
            {
                'id': i.invoice_number,
                'typology': i.typology,
                'start_date': i.start_date.strftime('%d/%m/%Y'),
                'end_date': i.end_date.strftime('%d/%m/%Y'),
                'total_patients': i.invoice_lines['total_patients'],
                'total_amount': i.invoice_lines['total_amount'],
                'status': i.get_status_display()
            }
            for i in query
        ]

        # Obtain the next invoices.
        next_invoices, cookies = check_can_create_invoice(TYPOLOGIES, user.care_house)

        care_houses = None
        if user.user_type == 'superuser':
            care_houses = [
                {
                    "code": c.identification_code,
                    "name": c.name
                }
                for c in CareHouse.objects.all()
            ]

        context = {
            'invoices': invoices,
            # 'datatable_url': '/api/datatables/finances/receipts/',
            'user': get_user_context(user),
            'next_invoices': next_invoices,
            "care_houses": care_houses
        }

        response = render(request, 'finances/html/care_house_receipts.html', context=context)
        for c in cookies:
            response.set_cookie(c['key'], c['value'])

        return response
    else:
        return redirect('/login/')
