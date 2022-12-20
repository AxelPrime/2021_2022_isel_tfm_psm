from asgiref.sync import sync_to_async
from django.contrib.auth import logout
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.api_responses.responses import success_response


@sync_to_async()
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_api(request):
    with transaction.atomic():
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        response = success_response(False, 'User Logged out')
        response.delete_cookie('userToken')
    return response
