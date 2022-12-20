from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.status import *

from user_management.models import CustomUser
from utils.api_responses.responses import success_response, error_response
from asgiref.sync import sync_to_async
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.user_context.user_context import get_user_context


@sync_to_async()
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_notifications_api(request):
    user = request.user  # type: CustomUser

    # Get the user data.
    user_data = get_user_context(user)

    resp_data = user_data['notification_data']

    return success_response(
        False,
        'Notifications obtained',
        resp_data
    )
