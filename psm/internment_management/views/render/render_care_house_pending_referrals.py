from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from internment_management.models import Referral, InternmentStatus
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USER_TYPES = [
    'care_house_staff',
]


@sync_to_async
def care_house_pending_referrals(request):
    if request.method == 'GET':
        user = request.user  # type: CustomUser
        if not user.is_authenticated or user.user_type not in ALLOWED_USER_TYPES:
            return redirect('/login/')

        context = {
            'datatable_url': '/api/datatables/referrals/awaits-opening/',
            'user': get_user_context(user),
            'status': [
                {
                    'label': 'awaits_reviewer',
                    'name': 'Aprovar'
                },
                {
                    'label': 'awaits_opening',
                    'name': 'Aguarda Vaga'
                },
                {
                    'label': 'referral_rejected',
                    'name': 'Rejeitar'
                },
            ]
        }

        return render(request, 'referrals/html/evaluate_active_referrals.html', context=context)
