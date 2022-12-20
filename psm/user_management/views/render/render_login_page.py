from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

from user_management.models import CustomUser

REDIRECTS = {
    'doctor': '/doctor/active-referrals/',
    'care_house_staff': '/care-house/active-internments/',
    'reviewer': '/reviewer/active-referrals/',
    'financial': '/financial/finances/monthly-receipts/',
    'superuser': '/superuser/doctor/referrals/',
}


def login_page(request):
    if request.method == 'GET':
        token = request.COOKIES.get('userToken')
        if request.user.is_authenticated or token is not None:
            try:
                user = Token.objects.get(key=token).user
            except Token.DoesNotExist:
                user = request.user  # type: CustomUser

            return redirect(REDIRECTS[user.user_type])
        # if request.user.is_anonymous:
        return render(request, 'user_management/html/login.html')
