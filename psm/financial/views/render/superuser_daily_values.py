from asgiref.sync import sync_to_async
from django.db import transaction
from django.shortcuts import redirect, render

from entities.models import CareHouse
from financial.models import MonthlyInvoice, DailyValue
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USERS = [
    'superuser'
]

DATE_FORMAT = "%d/%m/%Y"


@sync_to_async()
def daily_values_page(request):
    if request.method != 'GET':
        return redirect('/login/')

    # Obtain the request user.
    user = request.user  # type: CustomUser
    # Validate if the user has access permissions.
    if user.user_type not in ALLOWED_USERS:
        return redirect('/login/')

    # Begin transaction.
    with transaction.atomic():
        # Obtian the list of daily values.
        daily_values = [
            {
                "value": v.value,
                "start_date": v.start_date.strftime(DATE_FORMAT),
                "end_date": v.end_date.strftime(DATE_FORMAT) if v.end_date is not None else '-'
            }
            for v in DailyValue.objects.all().order_by('start_date')
        ]

    context = {
        "daily_values": daily_values
    }

    return render(request, "finances/html/superuser_daily_values.html", context=context)
