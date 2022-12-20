from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from entities.models import CareHouse
from financial.models import TypologyIIMonthlyStats
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USER_TYPES = [
    'financial',
    'superuser'
]


@sync_to_async()
def typology_ii_stats_page(request):
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USER_TYPES:
        return redirect('/login/')

    if request.method != 'GET':
        return redirect('/login')

    stats_data = [
        {
            'year': stats.year,
            'month_number': stats.month,
            'month': stats.get_month_display(),
            'total_patients': stats.total_patients,
            'total_amount': stats.total_amount
        }
        for stats in TypologyIIMonthlyStats.objects.all()
    ]

    context = {
        'user': get_user_context(user),
        'stats': stats_data,
    }

    return render(request, 'finances/html/financial_typology_ii.html', context=context)
