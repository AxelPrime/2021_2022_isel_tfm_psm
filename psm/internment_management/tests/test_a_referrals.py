from django.test import TestCase

from internment_management.models import Referral, CareHouseInternment, InternmentStatus
from utils.test_data import *


class TestReferrals(TestCase):
    """
    Class used to test the financial actions.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Method used to create the initial data for the tests.
        """

        print('\n------------------------------------------------------')
        print('-------------------Finances Tests-------------------')

        # Create the institutions.
        create_institutions()
        create_care_house()
        # Create the test users.
        create_test_users()
        # Create the possible states of the referral.
        create_test_status()
        # Create notification templates.
        create_notification_templates()
        # Create the test patients.
        create_test_patients()
        # Create the daily value to use in the invoices.
        create_test_daily_value()

    def create_referrals(self):
        """
        Create 2 referrals.
        """
        # Perform the login.
        login_data = {
            'email': 'doctor@mail.com',
            'password': 'caranguejo2k9',
            'remember_user': False,
        }
        login_response = self.client.post('/api/users/login/', data=login_data, content_type='application/json',
                                          follow=True)

        # Create the test data to send.
        file1 = open('files/test/file1.txt', 'rb')
        file2 = open('files/test/file2.txt', 'rb')

        # First referral data to send.
        referral_data_a = {
            'patient_name': 'Patient A',
            'patient_sns_number': '123456786',
            'patient_social_security_number': '123456786',
            'patient_phone_number': '123456786',
            'patient_birth_date': '04/01/1998',
            'patient_disease_type': '1',
            'patient_admission_diagnosis': 'Sicc',
            'patient_internment_duration': 'short',
            'patient_next_of_kin_name': 'Jane',
            'patient_next_of_kin_kinship': 'Cousin',
            'patient_next_of_kin_contact': 'mail@mail.com',
            'patient_internment_motive': 'Super sicc',
            'patient_other_diagnosis': '',
            'patient_medication': '',
            'patient_supervision': '1',
            'patient_social_security_status': 'Something',
            'patient_social_status': 'Something',
            'patient_origin_institution': '1',
            'patient_care_house': '1',
            'patient_address': 'Street',
            'patient_social_assistant': 'Mary',
            'patient_doctor_name': "",
            'patient_doctor_professional_certificate': "",
            'patient_responsibility_term': file1,
            'patient_supervision_scale': file2,
            'patient_gender': 'M',
            'patient_country': 'PT',
            'patient_nationality': 'PT',
            'patient_postal_code': '2620-486',
            'patient_locality': 'Ramada',
            'patient_subsystem': '543'
        }

        # Set the auth header.
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.client.cookies.get("userToken").value}'
        }

        # Create the first referral.
        response_a = self.client.post('/api/referrals/refer-patient/', data=referral_data_a, follow=True, **headers)
        # Verify if the request was a success.
        self.assertEquals(201, response_a.status_code)
        # Obtain the referral.
        referral_a = Referral.objects.all().order_by('id').last()
        # Verify that the referral exists.
        self.assertIsNotNone(referral_a)
        # Check the referral patient.
        self.assertEquals(referral_a.patient.sns_number, referral_data_a['patient_sns_number'])
        # Check the referral status.
        self.assertEquals(referral_a.current_status.label, 'awaits_care_house')

        file1.close()
        file2.close()

        # Create the test data to send.
        file1 = open('files/test/file1.txt', 'rb')
        file2 = open('files/test/file2.txt', 'rb')

        # The second referral data.
        referral_data_b = {
            'patient_name': 'Patient B',
            'patient_sns_number': '123456787',
            'patient_social_security_number': '123456787',
            'patient_phone_number': '123456787',
            'patient_birth_date': '23/02/1999',
            'patient_disease_type': '1',
            'patient_admission_diagnosis': 'Sicc',
            'patient_internment_duration': 'short',
            'patient_next_of_kin_name': 'Jane',
            'patient_next_of_kin_kinship': 'Cousin',
            'patient_next_of_kin_contact': 'mail@mail.com',
            'patient_internment_motive': 'Super sicc',
            'patient_other_diagnosis': '',
            'patient_medication': '',
            'patient_supervision': '1',
            'patient_social_security_status': 'Something',
            'patient_social_status': 'Something',
            'patient_origin_institution': '1',
            'patient_care_house': '1',
            'patient_address': 'Street',
            'patient_social_assistant': 'Mary',
            'patient_responsibility_term': file1,
            'patient_supervision_scale': file2,
            'patient_doctor_name': "",
            'patient_doctor_professional_certificate': "",
            'patient_gender': 'F',
            'patient_country': 'PT',
            'patient_nationality': 'PT',
            'patient_postal_code': '2620-486',
            'patient_locality': 'Ramada',
            'patient_subsystem': '543'
        }

        # Create the second referral.
        response_b = self.client.post('/api/referrals/refer-patient/', data=referral_data_b, follow=True, **headers)
        # Verify if the request was a success.
        self.assertEquals(201, response_b.status_code)
        # Obtain the referral.
        referral_b = Referral.objects.all().order_by('id').last()
        # Verify that the referral exists.
        self.assertIsNotNone(referral_b)
        # Check the referral patient.
        self.assertEquals(referral_b.patient.sns_number, referral_data_b['patient_sns_number'])
        # Check the referral status.
        self.assertEquals(referral_b.current_status.label, 'awaits_care_house')

        file1.close()
        file2.close()

    def care_house_approve_referral(self):
        referral = Referral.objects.all().order_by('id').last()
        referral_id = referral.id
        next_state = 'awaits_reviewer'

        # Perform the login.
        login_data = {
            'email': 'care_house@mail.com',
            'password': 'caranguejo2k9',
            'remember_user': False,
        }
        self.client.post('/api/users/login/', data=login_data, content_type='application/json', follow=True)

        request_body = {
            'status': next_state,
            'referrals': [referral.identifier],
            'rejection_reason': '',
        }

        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.client.cookies.get("userToken").value}'
        }
        response = self.client.post('/api/referrals/evaluate/', data=request_body, follow=True, **headers)

        self.assertEquals(200, response.status_code)

        ref = Referral.objects.get(id=referral_id)
        self.assertEquals(ref.current_status.label, next_state)

    def reviewer_approve_referral(self):
        referral = Referral.objects.all().order_by('id').last()
        referral_id = referral.id
        next_state = 'referral_approved'

        # Perform the login.
        login_data = {
            'email': 'reviewer@mail.com',
            'password': 'caranguejo2k9',
            'remember_user': False,
        }
        self.client.post('/api/users/login/', data=login_data, content_type='application/json', follow=True)

        request_body = {
            'status': next_state,
            'referrals': [referral.identifier],
            'rejection_reason': '',
        }

        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.client.cookies.get("userToken").value}'
        }
        response = self.client.post('/api/referrals/evaluate/', data=request_body, follow=True, **headers)

        self.assertEquals(200, response.status_code)

        ref = Referral.objects.get(id=referral_id)
        self.assertEquals(ref.current_status.label, next_state)

    def intern_patient(self):
        referral = Referral.objects.all().order_by('id').last()
        referral_id = referral.id

        # Perform the login.
        login_data = {
            'email': 'care_house@mail.com',
            'password': 'caranguejo2k9',
            'remember_user': False,
        }
        self.client.post('/api/users/login/', data=login_data, content_type='application/json', follow=True)

        request_body = {
            'referrals': [
                CareHouseInternment.objects.get(referral__id=referral_id).identifier
            ]
        }

        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.client.cookies.get("userToken").value}'
        }
        response = self.client.post('/api/internments/register-internments/', data=request_body, follow=True, **headers)
        self.assertEquals(200, response.status_code)

        internment = CareHouseInternment.objects.get(referral__id=referral_id)
        self.assertEquals('interned', internment.current_status.label)
        self.assertIsNotNone(internment.admission_date)

    def test_referral_process(self):
        self.create_referrals()
        self.care_house_approve_referral()
        self.reviewer_approve_referral()
        self.intern_patient()
