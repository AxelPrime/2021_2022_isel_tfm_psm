import uuid
from datetime import datetime

from django.core.files.base import File
from django.db import transaction

from entities.models import MedicalInstitution, CareHouse
from internment_management.models import Referral, InternmentStatus, Patient, CareHouseInternment, ActivityLog
from user_management.models import CustomUser

# PATIENT_DATA = [
# {
#     'name': 'Patient A',
#     'id': '1',
#     'sns_number': '123456789',
#     'social_security_number': '123456789',
#     'phone_number': '123456789',
#     'referral_id': '1',
#     'process_number': 1,
#     'referral_date': datetime(year=2022, month=1, day=1),
#     'internment_id': '1',
#     'log_data': [
#         {
#             'identifier': uuid.uuid4(),
#             'action': 'Entrada',
#             'activity_type': 'entry',
#             'date': datetime(year=2022, month=1, day=1)
#         }
#     ]
# },
# {
#     'name': 'Patient B',
#     'id': '2',
#     'sns_number': '123456780',
#     'social_security_number': '123456780',
#     'phone_number': '123456780',
#     'referral_id': '2',
#     'process_number': 2,
#     'referral_date': datetime(year=2022, month=5, day=3),
#     'internment_id': '2',
#     'log_data': [
#         {
#             'identifier': uuid.uuid4(),
#             'action': 'Entrada',
#             'activity_type': 'entry',
#             'date': datetime(year=2022, month=5, day=3)
#         },
#         {
#             'identifier': uuid.uuid4(),
#             'action': 'Consulta Externa',
#             'activity_type': 'temporary_leave',
#             'date': datetime(year=2022, month=5, day=7)
#         },
#         {
#             'identifier': uuid.uuid4(),
#             'action': 'Internado',
#             'activity_type': 'return',
#             'date': datetime(year=2022, month=5, day=11)
#         }
#     ]
# },
# {
#     'name': 'Patient C',
#     'id': '3',
#     'sns_number': '123456781',
#     'social_security_number': '123456781',
#     'phone_number': '123456781',
#     'referral_id': '3',
#     'process_number': 3,
#     'referral_date': datetime(year=2022, month=2, day=3),
#     'internment_id': '3',
#     'log_data': [
#         {
#             'identifier': uuid.uuid4(),
#             'action': 'Entrada',
#             'activity_type': 'entry',
#             'date': datetime(year=2022, month=2, day=3)
#         },
#         {
#             'identifier': uuid.uuid4(),
#             'action': 'Consulta Externa',
#             'activity_type': 'temporary_leave',
#             'date': datetime(year=2022, month=4, day=20)
#         },
#         {
#             'identifier': uuid.uuid4(),
#             'action': 'Internado',
#             'activity_type': 'return',
#             'date': datetime(year=2022, month=5, day=10)
#         }
#     ]
# },
#     {
#         'name': 'Patient D',
#         'id': '4',
#         'sns_number': '123456782',
#         'social_security_number': '123456782',
#         'phone_number': '123456782',
#         'referral_id': '4',
#         'process_number': 4,
#         'referral_date': datetime(year=2022, month=2, day=1),
#         'internment_id': '4',
#         'leave_date': datetime(year=2022, month=4, day=15),
#         'log_data': [
#             {
#                 'identifier': uuid.uuid4(),
#                 'action': 'Entrada',
#                 'activity_type': 'entry',
#                 'date': datetime(year=2022, month=2, day=3)
#             },
#             {
#                 'identifier': uuid.uuid4(),
#                 'action': 'Falecido',
#                 'activity_type': 'exit',
#                 'date': datetime(year=2022, month=5, day=15)
#             },
#         ]
#     }
# ]

PATIENT_DATA = [
    {
        'name': 'Patient E',
        'id': '5',
        'sns_number': '123456783',
        'social_security_number': '123456783',
        'phone_number': '123456783',
        'referral_id': '5',
        'process_number': 5,
        'referral_date': datetime(year=2022, month=4, day=20),
        'internment_id': '5',
        'log_data': [
            {
                'identifier': uuid.uuid4(),
                'action': 'Entrada',
                'activity_type': 'entry',
                'date': datetime(year=2022, month=5, day=1)
            }
        ]
    },
    {
        'name': 'Patient F',
        'id': '6',
        'sns_number': '123456784',
        'social_security_number': '123456784',
        'phone_number': '123456784',
        'referral_id': '6',
        'process_number': 6,
        'referral_date': datetime(year=2022, month=1, day=1),
        'internment_id': '6',
        'log_data': [
            {
                'identifier': uuid.uuid4(),
                'action': 'Entrada',
                'activity_type': 'entry',
                'date': datetime(year=2022, month=1, day=1)
            },
            {
                'identifier': uuid.uuid4(),
                'action': 'Transferência',
                'activity_type': 'exit',
                'date': datetime(year=2022, month=5, day=20)
            }
        ]
    },
]


def run():
    with transaction.atomic():
        for p in PATIENT_DATA:

            # Create a referral.
            patient = Patient.objects.create(
                identifier=p['id'],
                name=p['name'],
                sns_number=p['sns_number'],
                social_security_number=p['social_security_number'],
                phone_number=p['phone_number'],
                address='Street',
                birth_date=datetime(year=1998, month=1, day=4).date(),
            )

            # Create the test data to send.
            file1 = open('files/test/file1.txt', 'rb')
            file2 = open('files/test/file2.txt', 'rb')

            referral = Referral(
                identifier=p['referral_id'],
                patient=patient,
                origin_institution=MedicalInstitution.objects.get(institution_code='2'),
                care_house=CareHouse.objects.get(identification_code='abcd1234'),
                typology='II',
                admission_diagnosis='Sicc',
                process_number=p['process_number'],
                disease_type='1',
                responsibility_term=File(file1),
                supervision_scale=File(file2),
                family_situation='Family',
                relative_name='',
                relative_kinship='',
                relative_contact='',
                social_assistant='',
                supervision_grade='1',
                referral_motive='Yes',
                other_diagnosis='',
                social_situation='Very',
                internment_duration='short',
                medication='',
                referral_date=p['referral_date'],
                current_status=InternmentStatus.objects.get(label="referral_approved"),
                referred_by=CustomUser.objects.get(email='admin@mail.com')
            )
            referral.save()

            internment = CareHouseInternment(
                identifier=p['internment_id'],
                referral=referral,
                admitted_by=CustomUser.objects.get(email='care_house@mail.com'),
                current_status=InternmentStatus.objects.get(label='interned'),
                admission_date=p['referral_date'],
                leave_date=p.get('leave_date')
            )
            internment.save()

            for a in p['log_data']:
                activity_log = ActivityLog(
                    identifier=a['identifier'],
                    internment=internment,
                    executed_by=CustomUser.objects.get(email='care_house@mail.com'),
                    action=a['action'],
                    activity_type=a['activity_type'],
                    log_date=a['date']
                )
                activity_log.save()
