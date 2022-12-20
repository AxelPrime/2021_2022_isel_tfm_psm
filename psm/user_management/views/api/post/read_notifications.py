from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.status import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import sync_to_async

from user_management.models import Notifications
from utils.api_responses.responses import error_response, success_response


@sync_to_async()
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def read_notification_api(request):
    # Get the notification id.
    notification_id = request.data.get("notification_id")
    if not notification_id:
        return error_response(
            HTTP_400_BAD_REQUEST,
            "Pedido inválido"
        )

    with transaction.atomic():
        try:
            notification = Notifications.objects.get(identifier=notification_id)
        except Notifications.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                "Notificação não encontrada."
            )

        notification.display = False
        notification.save()

    return success_response(False, "Notificação lida com sucesso")
