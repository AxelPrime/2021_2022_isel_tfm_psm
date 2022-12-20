from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.status import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from internment_management.models import Patient
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from asgiref.sync import sync_to_async
from utils.patient_db.patient_api import get_patient_interface

ALLOWED_USER_TYPES = [
    'doctor',
    'superuser'
]


@sync_to_async
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def patient_data_api(request):
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissões de acesso.'
        )

    sns_number = request.GET.get('sns_number')
    if not sns_number:
        return error_response(
            HTTP_400_BAD_REQUEST,
            'É necessário indicar o nº de SNS do paciente'
        )

    with transaction.atomic():
        try:
            patient = Patient.objects.get(sns_number=sns_number)
        except Patient.DoesNotExist:
            patient = None

        patient_data = get_patient_interface().search_patient(sns_number)

        if patient_data is None:
            return error_response(
                HTTP_404_NOT_FOUND,
                "Paciente não encontrado no sistema"
            )

        patient_data["social_sec_number"] = patient.social_security_number if patient is not None else ''

    data = {
        'patient': patient_data,
    }

    return success_response(False, 'Paciente obtido com sucesso', data)
