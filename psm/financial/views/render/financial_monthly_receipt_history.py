from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from financial.models import MonthlyInvoice
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USERS = [
    'financial',
    'superuser',
]


@sync_to_async()
def financial_receipt_history_page(request):
    if request.method == 'GET':
        user = request.user  # type: CustomUser
        if not user.is_authenticated or user.user_type not in ALLOWED_USERS:
            return redirect('/login/')

        # The active status.
        active_status = ['paid', 'rejected']

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
            for i in MonthlyInvoice.objects.filter(
                status__in=active_status
            )
        ]
        context = {
            'invoices': invoices,
            'user': get_user_context(user),
        }

        return render(request, 'finances/html/financial_monthly_receipt_history.html', context=context)

    else:
        return redirect('/login/')
