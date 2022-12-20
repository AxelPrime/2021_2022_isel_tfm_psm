from asgiref.sync import sync_to_async
from django.shortcuts import render, redirect
from entities.models import CareHouse, MedicalInstitution
from internment_management.models import Referral
from user_management.models import CustomUser
from utils.user_context import get_user_context

ALLOWED_USER_TYPES = [
    'superuser'
]


@sync_to_async
def superuser_doctor_referrals_page(request):
    # Obtain the request user.
    user = request.user  # type: CustomUser
    # Check if the request method is valid.
    if request.method == 'GET':
        # Validate the user.
        if not user.is_authenticated or user.user_type not in ALLOWED_USER_TYPES:
            return redirect('/login/')

        # Obtain the Care Houses for referrals.
        care_houses = [
            {
                "name": c.name,
                "code": c.identification_code
            }
            for c in CareHouse.objects.all()
        ]
        # Obtain the institutions for referrals.
        institutions = [
            {
                "name": i.name,
                "code": i.institution_code
            }
            for i in MedicalInstitution.objects.all()
        ]

        # Set the context.
        context = {
            'user': get_user_context(user),
            "care_houses": care_houses,
            "institutions": institutions,
            # "referrals": referrals
            'datatable_url': '/api/datatables/referrals/active/'
        }
        # Render the template.
        return render(request, 'referrals/html/superuser_doctor_active_referrals.html', context=context)
    # Redirect to login page.
    return redirect('/login/')
