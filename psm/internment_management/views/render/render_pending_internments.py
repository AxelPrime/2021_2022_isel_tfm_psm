from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from internment_management.models import Referral, CareHouseInternment
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USER_TYPES = [
    'care_house_staff',
    'superuser'
]


@sync_to_async
def pending_internments(request):
    if request.method == 'GET':
        user = request.user  # type: CustomUser
        if not user.is_authenticated or user.user_type not in ALLOWED_USER_TYPES:
            return redirect('/login/')

        context = {
            # 'referrals': referrals_data,
            'user': get_user_context(user),
            'datatable_url': '/api/datatables/internments/awaits-entrance/'
        }

        return render(request, 'internments/html/care_house_pending_internments.html', context=context)
