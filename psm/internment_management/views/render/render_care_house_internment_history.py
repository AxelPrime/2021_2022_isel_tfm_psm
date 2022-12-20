from asgiref.sync import sync_to_async
from django.shortcuts import redirect, render

from internment_management.models import Referral, InternmentStatus
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USER_TYPES = [
    'care_house_staff',
    'superuser',
]


@sync_to_async
def internment_history_page(request):
    if request.method == 'GET':
        user = request.user  # type: CustomUser
        if not user.is_authenticated or user.user_type not in ALLOWED_USER_TYPES:
            return redirect('/login/')

        context = {
            'datatable_url': '/api/datatables/internments/history/',
            'user': get_user_context(user),
        }

        return render(request, 'internments/html/internment_history.html', context=context)
