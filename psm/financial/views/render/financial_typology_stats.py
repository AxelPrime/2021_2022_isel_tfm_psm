from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from entities.models import CareHouse
from financial.models import TypologyStats
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USER_TYPES = [
    'financial',
    'superuser'
]


@sync_to_async()
def typology_stats_page(request):
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USER_TYPES:
        return redirect('/login/')

    if request.method != 'GET':
        return redirect('/login')

    stats_data = [
        {
            'year': stats.year,
            'created': stats.created,
            'modified': stats.modified
        }
        for stats in TypologyStats.objects.all()
    ]

    context = {
        'user': get_user_context(user),
        'stats': stats_data,
        'typology': ['I', 'II', 'III'],
        'typology_combo': ['I + II + III', 'I + III'],
        'care_houses': [
            {
                'id': c.identification_code,
                'name': c.name
            }
            for c in CareHouse.objects.all()
        ]
    }

    return render(request, 'finances/html/financial_typology_stats.html', context=context)
