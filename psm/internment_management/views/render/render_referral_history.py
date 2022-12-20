from asgiref.sync import sync_to_async
from django.shortcuts import render, redirect

from user_management.models import CustomUser
from utils.user_context import get_user_context


@sync_to_async
def referral_history(request):
    # Obtain the user of the request.
    user = request.user  # type: CustomUser
    # Verify if the request is a GET
    if request.method == 'GET':
        # Validate if the user can access this page.
        if user.is_authenticated:
            # Set the context.
            context = {
                'user': get_user_context(user),
                # "referrals": referrals
                'datatable_url': '/api/datatables/referrals/history/'
            }
            # Render the template.
            return render(request, 'referrals/html/referral_history.html', context=context)
    # Redirect to login page.
    return redirect('/login/')
