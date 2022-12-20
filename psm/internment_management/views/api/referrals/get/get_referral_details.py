from asgiref.sync import sync_to_async
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from internment_management.models import Referral
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response

ALLOWED_USER_TYPES = [
    'doctor',
    'care_house_staff',
    'reviewer',
    'financial',
    'superuser',
]


@sync_to_async
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_referral_details_api(request):
    # Obtain the authenticated user.
    user = request.user  # type: CustomUser

    # Verify if the user ha access to this data.
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(HTTP_401_UNAUTHORIZED, 'You do not have permission to access this content')

    # Obtain the referrals ID from the request.
    referral_id = request.GET.get('referral_id')
    if not referral_id:
        return error_response(HTTP_400_BAD_REQUEST, "'referral' must be present")

    # Start a transaction.
    with transaction.atomic():
        # Try to obtain the referral.
        try:
            referral = Referral.objects.get(identifier=referral_id)
        except Referral.DoesNotExist:
            return error_response(HTTP_404_NOT_FOUND, 'Referral does not exist.')

        # Obtain the details of the referral.
        referral_data = {
            'patient_name': referral.patient.name,
            'patient_sns_number': referral.patient.sns_number,
            'patient_social_security_number': referral.patient.social_security_number,
            'patient_phone_number': referral.patient.phone_number,
            'patient_address': referral.patient.address,
            'patient_birth_date': referral.patient.birth_date.strftime('%d/%m/%Y'),
            'origin_institution_name': referral.origin_institution.name,
            'origin_institution_code': referral.origin_institution.institution_code,
            'care_house_name': referral.care_house.name,
            'care_house_code': referral.care_house.identification_code,
            'typology': referral.typology,
            'admission_diagnosis': referral.admission_diagnosis,
            'disease_type': referral.get_disease_type_display(),
            'process_number': referral.process_number,
            'family_situation': referral.family_situation,
            'relative_name': referral.relative_name if referral.relative_name else '-',
            'relative_kinship': referral.relative_kinship if referral.relative_kinship else '-',
            'relative_contact': referral.relative_contact if referral.relative_contact else '-',
            'social_assistant': referral.social_assistant,
            'supervision_grade': referral.get_supervision_grade_display(),
            'referral_motive': referral.referral_motive,
            'other_diagnosis': referral.other_diagnosis if referral.other_diagnosis else '-',
            'social_situation': referral.social_situation,
            'internment_duration': referral.get_internment_duration_display(),
            'medication': referral.medication if referral.medication else '-',
            'referral_date': referral.referral_date.strftime('%Y-%m-%d %H:%M'),
            'approval_date': referral.approval_date.strftime('%Y-%m-%d %H:%M') if referral.approval_date else '-',
            'current_status': referral.current_status.name,
            'referred_by': f"{referral.referred_by.first_name} {referral.referred_by.last_name}",
            'patient_postal_code': referral.patient.postal_code,
            'patient_locality': referral.patient.locality,
            'patient_subsystem': referral.patient.get_subsystem_display(),
        }

    # Return success response.
    return success_response(False, 'Referral data obtained', data={"referral_data": referral_data})