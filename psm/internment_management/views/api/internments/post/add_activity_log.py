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
from internment_management.serializers.internments import AddActivityLogSerializer
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response

ALLOWED_USERS = [
    'care_house_staff',
    'superuser'
]


@sync_to_async
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_activity_log_api(request):
    # Obtain the authenticated user.
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USERS:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissão de acesso'
        )

    # Serialize the request data.
    serialized_request = AddActivityLogSerializer(data=request.data)
    if not serialized_request.is_valid():
        return error_response(HTTP_400_BAD_REQUEST, 'Pedido inválido', data=serialized_request.errors)

    # Obtain the validated data.
    valid_data = serialized_request.validated_data

    # Begin transaction.
    with transaction.atomic():
        # Obtain the internment.
        try:
            internment = CareHouseInternment.objects.get(identifier=valid_data['internment_id'])
        except CareHouseInternment.DoesNotExist:
            return error_response(HTTP_404_NOT_FOUND, 'Internamento não encontrado')

        if internment.current_status.next_states is None or valid_data['next_state'] not in internment.current_status.next_states:
            return error_response(HTTP_400_BAD_REQUEST, 'Estado inválido')

        # Obtain the next status object.
        next_status = InternmentStatus.objects.get(label=valid_data['next_state'])

        # Check if the status is terminal.
        if next_status.next_states is None:
            activity_type = 'exit'
            internment.leave_date = datetime.utcnow()
        elif next_status.label == 'interned':
            activity_type = 'return'
        else:
            activity_type = 'temporary_leave'

        internment.current_status = next_status
        internment.save()

        # Create the activity log.
        activity_log = ActivityLog(
            identifier=uuid.uuid4(),
            internment=internment,
            executed_by=user,
            action=internment.current_status.name,
            activity_type=activity_type,
            description=valid_data['description'],
            log_date=timezone.now()
        )
        activity_log.save()

    return success_response(True, 'Registo creado')