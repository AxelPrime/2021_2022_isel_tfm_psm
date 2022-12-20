from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from entities.models import CareHouse
from financial.models import YearlyInvoice
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USER_TYPES = [
    'financial',
    'superuser'
]

@sync_to_async()
def yearly_invoices_page(request):
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USER_TYPES:
        return redirect('/login/')

    if request.method != 'GET':
        return redirect('/login')

    # Obtain the list of invoices.
    invoices = [
        {
            'year': i.year,
            'total_amount': i.total_amount,
            'invoice_number': i.invoice_number
        }
        for i in YearlyInvoice.objects.all()
    ]

    # Prepare the context data.
    context = {
        'user': get_user_context(user),
        'invoices': invoices
    }

    # Render the page.
    return render(request, 'finances/html/financial_yearly_incoices.html', context=context)
