from asgiref.sync import sync_to_async
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from internment_management.models import InternmentStatus, CareHouseInternment, ActivityLog
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from dateutil import tz

ALLOWED_USERS = [
    'care_house_staff',
    'financial',
    'superuser'
]

UTC_TZ = tz.gettz('UTC')
PORTUGAL_TZ = tz.gettz("Europe/Lisbon")


@sync_to_async
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def activity_log_api(request):
    # Obtain the authenticated user.
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USERS:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissão de acesso'
        )

    # Obtain the internment ID.
    internment_id = request.GET.get('internment_id')
    if not internment_id:
        return error_response(HTTP_400_BAD_REQUEST, 'É necessário indicar o internamento')

    # Begin transaction.
    with transaction.atomic():
        # Obtain the internment object.
        try:
            internment = CareHouseInternment.objects.get(identifier=internment_id)
        except CareHouseInternment.DoesNotExist:
            return error_response(HTTP_404_NOT_FOUND, 'Internamento não encontrado')

        # Obtain the activity logs.
        activity = [
            [
                log.action,
                log.description if log.description else '-',
                f"{log.executed_by.first_name} {log.executed_by.last_name}",
                log.log_date.replace(tzinfo=UTC_TZ).astimezone(PORTUGAL_TZ).strftime('%d/%m/%Y %H:%M:%S')
            ]
            for log in ActivityLog.objects.filter(internment=internment)
        ]

        if internment.current_status.next_states is not None:
            is_terminal = False
            next_sates = [
                {
                    'label': status.label,
                    'name': status.name
                }
                for status in InternmentStatus.objects.filter(label__in=internment.current_status.next_states)
            ]
        else:
            is_terminal = True
            next_sates = []

        # Create the response data.
        response_data = {
            'logs': activity,
            'patient_name': internment.referral.patient.name,
            'is_terminal': is_terminal,
            'next_states': next_sates
        }

    return success_response(False, "Registo obtido", data=response_data)