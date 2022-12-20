from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from internment_management.models import Referral, InternmentStatus
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USER_TYPES = [
    'reviewer',
]


@sync_to_async
def reviewer_pending_referrals(request):
    if request.method == 'GET':
        user = request.user  # type: CustomUser
        if not user.is_authenticated or user.user_type not in ALLOWED_USER_TYPES:
            return redirect('/login/')

        context = {
            # 'referrals': referrals_data,
            'datatable_url': '/api/datatables/referrals/awaits-approval/',
            'user': get_user_context(user),
            'status': [
                {
                    'label': 'referral_approved',
                    'name': 'Aprovar'
                },
                {
                    'label': 'referral_rejected',
                    'name': 'Rejeitar'
                },
            ]
        }

        return render(request, 'referrals/html/evaluate_active_referrals.html', context=context)
