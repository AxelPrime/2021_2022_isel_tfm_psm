from datetime import datetime

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.status import *

from user_management.models import CustomUser
from user_management.serializers.api.post import LoginSerializer
from utils.api_responses.responses import error_response, success_response

REDIRECTS = {
    'doctor': '/doctor/active-referrals/',
    'care_house_staff': '/care-house/active-internments/',
    'reviewer': '/reviewer/active-referrals/',
    'financial': '/financial/finances/monthly-receipts/',
    'superuser': '/superuser/doctor/referrals/',
}


@sync_to_async()
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_api(request):
    serialized_request = LoginSerializer(data=request.data)
    if not serialized_request.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            "Todos os campos devem ser preenchidos",
            serialized_request.errors
        )
    valid_data = serialized_request.validated_data

    user = authenticate(username=valid_data['email'], password=valid_data['password'])  # type: CustomUser

    if user is not None:
        login(request, user)
        if valid_data['remember_user']:
            date_expire = datetime(year=2100, month=1, day=1)
        else:
            date_expire = None
        token, _ = Token.objects.get_or_create(user=user)
        response = success_response(False, 'User logged in', data={'redirect_to': REDIRECTS[user.user_type]})
        response.set_cookie('userToken', token.key, expires=date_expire)
        return response

    return error_response(HTTP_401_UNAUTHORIZED, 'User credentials invalid')
