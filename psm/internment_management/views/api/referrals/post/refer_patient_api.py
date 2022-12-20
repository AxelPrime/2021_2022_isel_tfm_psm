import random
from datetime import datetime
from hashlib import sha256

from asgiref.sync import sync_to_async
from django.db import transaction
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from entities.models import MedicalInstitution, CareHouse
from internment_management.models import Patient, Referral, CareHouseInternment, InternmentStatus
from internment_management.serializers.referral import ReferPatientFileSerializer, ReferPatientDataSerializer
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from utils.notifications.notifications import NotificationsManager
from utils.patient_db.patient_api import get_patient_interface

ALLOWED_USER_TYPES = [
    'doctor',
    'superuser'
]
NOTIFICATION_CREATE_TEMPLATE = "REFERRAL_CREATION"
NOTIFICATION_CREATE_TYPE = "referral_creation"


@sync_to_async
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def refer_patient_api(request):
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(HTTP_401_UNAUTHORIZED, 'Tipo de utilizador inválido')

    # Validate the form data.
    serialized_request_data = ReferPatientDataSerializer(data=request.POST)
    if not serialized_request_data.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'É necessário preencher todos os campos',
            serialized_request_data.errors
        )
    # Obtain the validated JSON data.
    valid_data = serialized_request_data.validated_data

    # Validate the files data.
    serialized_request_files = ReferPatientFileSerializer(data=request.FILES)
    if not serialized_request_files.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'É necessário enviar todos os ficheiros',
            serialized_request_data.errors
        )
    # Obtain the validated JSON file data.
    valid_files = serialized_request_files.validated_data

    notifications_manager = NotificationsManager("", NOTIFICATION_CREATE_TYPE)

    with transaction.atomic():
        # Obtain the patient from the DB or create an entry.
        try:
            patient = Patient.objects.get(sns_number=valid_data['patient_sns_number'])
        except Patient.DoesNotExist:
            patient = Patient(
                identifier=sha256(f"{datetime.utcnow()}".encode()).hexdigest(),
                name=valid_data["patient_name"],
                sns_number=valid_data["patient_sns_number"],
                social_security_number=valid_data["patient_social_security_number"],
                phone_number=valid_data['patient_phone_number'],
                address=valid_data["patient_address"],
                birth_date=valid_data["patient_birth_date"],
                gender=valid_data["patient_gender"],
                country=valid_data["patient_country"],
                nationality=valid_data["patient_nationality"],
                postal_code=valid_data["patient_postal_code"],
                locality=valid_data["patient_locality"],
                subsystem=valid_data["patient_subsystem"],
            )
            patient.save()

        # Verify if there is an open referral for this patient.
        try:
            Referral.objects.get(
                patient=patient,
                current_status__label__in=["awaits_care_house", "awaits_opening", "awaits_hff"]
            )
            return error_response(
                HTTP_409_CONFLICT,
                'Já existe uma referenciação aberta com este paciente.'
            )
        except Referral.DoesNotExist:
            pass

        # Verify if the patient is already in a Care House.
        try:
            CareHouseInternment.objects.get(
                referral__patient=patient,
                current_status__label__in=["awaits_entry", "interned", "external_consultation"]
            )
            return error_response(
                HTTP_409_CONFLICT,
                "O paciente já se encontra internado numa Casa de Saúde"
            )
        except CareHouseInternment.DoesNotExist:
            pass

        # Obtain the origin institution.
        medical_institution = MedicalInstitution.objects.get(
            institution_code=valid_data["patient_origin_institution"]
        )

        if user.user_type == 'superuser':
            doctor_name = valid_data["patient_doctor_name"]
            doctor_professional_certificate = valid_data["patient_doctor_professional_certificate"]
        else:
            doctor_name = f"{user.first_name} {user.last_name}"
            doctor_professional_certificate = user.professional_certificate

        # Obtain the Care House object.
        care_house = CareHouse.objects.get(identification_code=valid_data["patient_care_house"])
        # Create the referral.
        referral = Referral(
            identifier=sha256(f"{patient.sns_number}{datetime.utcnow()}".encode()).hexdigest(),
            patient=patient,
            origin_institution=medical_institution,
            care_house=care_house,
            typology="II" if medical_institution.institution_code != '1' else 'III',
            admission_diagnosis=valid_data['patient_admission_diagnosis'],
            process_number=str(random.randint(0, 100000)),
            disease_type=valid_data['patient_disease_type'],
            responsibility_term=valid_files['patient_responsibility_term'],
            supervision_scale=valid_files['patient_supervision_scale'],
            family_situation=valid_data["patient_social_status"],
            relative_name=valid_data["patient_next_of_kin_name"],
            relative_kinship=valid_data["patient_next_of_kin_kinship"],
            relative_contact=valid_data["patient_next_of_kin_contact"],
            social_assistant=valid_data["patient_social_assistant"],
            supervision_grade=valid_data["patient_supervision"],
            referral_motive=valid_data["patient_internment_motive"],
            other_diagnosis=valid_data["patient_other_diagnosis"],
            social_situation=valid_data["patient_social_security_status"],
            internment_duration=valid_data["patient_internment_duration"],
            medication=valid_data["patient_medication"],
            referral_date=timezone.now(),
            current_status=InternmentStatus.objects.get(label="awaits_care_house"),
            referred_by=user,
            doctor_name=doctor_name,
            doctor_professional_certificate=doctor_professional_certificate
        )
        referral.save()

        notifications_manager.create_notification(
            notification_for="care_house_staff",
            template=NOTIFICATION_CREATE_TEMPLATE,
            readable=False,
            redirect_to="/care-house/pending-referrals/",
            referral=referral,
            invoice=None,
            care_house=care_house
        )

        if valid_data['create_db']:
            get_patient_interface().add_patient(
                patient.sns_number,
                patient.name,
                patient.gender,
                patient.phone_number,
                patient.birth_date.strftime("%Y-%m-%d"),
                patient.address,
                patient.postal_code,
                patient.locality,
                patient.country,
                patient.nationality,
                patient.subsystem,
            )

    return success_response(
        True,
        'Referenciação criada com suecesso',
        data={
            'name': referral.patient.name,
            'sns': referral.patient.sns_number,
            'social_sec': referral.patient.social_security_number,
            'origin_institution': referral.origin_institution.name,
            'care_house': referral.care_house.name,
            'typology': referral.typology,
            'status': referral.current_status.name,
            'id': referral.identifier
        }
    )
