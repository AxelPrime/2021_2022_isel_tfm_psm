import uuid
from datetime import datetime

from asgiref.sync import sync_to_async
from django.db import transaction
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from internment_management.models import InternmentStatus, CareHouseInternment, ActivityLog
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from internment_management.serializers.internments import RegisterInternmentsSerializer
from utils.notifications.notifications import NotificationsManager

ALLOWED_USERS = [
    'care_house_staff',
    'superuser'
]
NOTIFICATION_READ_TYPE = ["referral_evaluation"]


@sync_to_async
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def register_internment_api(request):
    # Obtain the authenticated user.
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USERS:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissão de acesso'
        )

    # Obtain the referrals.
    serialized_request = RegisterInternmentsSerializer(data=request.data)
    if not serialized_request.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Pedido inválido',
            serialized_request.errors
        )
    valid_data = serialized_request.validated_data
    internments = valid_data['referrals']
    notifications_manager = NotificationsManager(read_type=NOTIFICATION_READ_TYPE)
    # Start a transaction
    with transaction.atomic():
        next_status = 'interned'
        internments_data = CareHouseInternment.objects.filter(identifier__in=internments)
        time_now = timezone.now()
        # The activity logs list to add.
        activity_logs = []

        # Verify if the next status is valid.
        for ref in internments_data:
            if next_status not in ref.current_status.next_states:
                return error_response(
                    HTTP_400_BAD_REQUEST,
                    'Estado seguinte inválido'
                )

            activity_logs.append(
                ActivityLog(
                    identifier=uuid.uuid4(),
                    internment=ref,
                    executed_by=user,
                    action='Entrada',
                    activity_type='entry',
                    log_date=time_now
                )
            )
            notifications_manager.hide_notification(user.user_type, referral=ref.referral)

        # Set the next status.
        internments_data.update(
            current_status=InternmentStatus.objects.get(label=next_status),
            admission_date=time_now,
            admitted_by=user
        )

        ActivityLog.objects.bulk_create(activity_logs)

    # Success response.
    return success_response(
        False,
        'Estado alterado'
    )
