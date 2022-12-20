from django.test import TestCase

from entities.models import CareHouse
from user_management.models import CustomUser


class RenderTests(TestCase):
    """
    Class to test the correct render for each method.
    """

    @classmethod
    def setUpTestData(cls):
        print('\n------------------------------------------------------')
        print('---------------------Render Tests---------------------')

        # Create the test Doctor.
        print("Creating test Doctor...")
        doctor = CustomUser.objects.create_user(
            'doctor@mail.com',
            'caranguejo2k9',
            'Mr',
            'Doctor'
        )
        doctor.user_type = 'doctor'
        doctor.professional_certificate = 'abc123'
        doctor.save()

        # Create the test reviewer.
        print("Creating test Reviewer...")
        reviewer = CustomUser.objects.create_user(
            'reviewer@mail.com',
            'caranguejo2k9',
            'Mr',
            'Reviewer'
        )
        reviewer.user_type = 'reviewer'
        reviewer.save()

        # Create the test care house staff.
        print("Creating test Care House Staff...")
        care_house = CustomUser.objects.create_user(
            'care_house@mail.com',
            'caranguejo2k9',
            'Mr',
            'Care House'
        )
        care_house.user_type = 'care_house_staff'
        care_house.care_house = CareHouse.objects.create(identification_code='1234', name='Telhal', address='Street')
        care_house.save()

    # Test the rendered template for Doctor Active Referrals.
    def test_render_doctor_active_referrals(self):
        login = self.client.login(email='doctor@mail.com', password='caranguejo2k9')
        response = self.client.get('/doctor/active-referrals/')
        self.assertTemplateUsed(response, 'referrals/html/doctor_active_referrals.html')

    # Test the rendered template for Doctor Referral History.
    def test_render_doctor_referral_history(self):
        login = self.client.login(email='doctor@mail.com', password='caranguejo2k9')
        response = self.client.get('/referrals/history/')
        self.assertTemplateUsed(response, 'referrals/html/referral_history.html')

    # Test the rendered template for Care House Pending Referrals.
    def test_render_care_house_pending_referrals(self):
        login = self.client.login(email='care_house@mail.com', password='caranguejo2k9')
        response = self.client.get('/care-house/pending-referrals/')
        self.assertTemplateUsed(response, 'referrals/html/evaluate_active_referrals.html')

    # Test the rendered template for Care House Pending Internments.
    def test_render_care_house_pending_internments(self):
        login = self.client.login(email='care_house@mail.com', password='caranguejo2k9')
        response = self.client.get('/care-house/pending-internments/')
        self.assertTemplateUsed(response, 'internments/html/care_house_pending_internments.html')

    # Test the rendered template for Care House Referral History.
    def test_render_care_house_referral_history(self):
        login = self.client.login(email='care_house@mail.com', password='caranguejo2k9')
        response = self.client.get('/referrals/history/')
        self.assertTemplateUsed(response, 'referrals/html/referral_history.html')

    # Test the rendered template for Reviewer Active Referrals.
    def test_render_reviewer_active_referrals(self):
        login = self.client.login(email='reviewer@mail.com', password='caranguejo2k9')
        response = self.client.get('/reviewer/active-referrals/')
        self.assertTemplateUsed(response, 'referrals/html/evaluate_active_referrals.html')

    # Test the rendered template for Reviewer Referral History.
    def test_render_reviewer_referral_history(self):
        login = self.client.login(email='reviewer@mail.com', password='caranguejo2k9')
        response = self.client.get('/referrals/history/')
        self.assertTemplateUsed(response, 'referrals/html/referral_history.html')

    # Test the rendered template for Reviewer Referral History.
    def test_render_care_house_active_internments(self):
        login = self.client.login(email='care_house@mail.com', password='caranguejo2k9')
        response = self.client.get('/care-house/active-internments/')
        self.assertTemplateUsed(response, 'internments/html/active_internments.html')

    # Test the rendered template for Reviewer Referral History.
    def test_render_care_house_internments_history(self):
        login = self.client.login(email='care_house@mail.com', password='caranguejo2k9')
        response = self.client.get('/care-house/internment-history/')
        self.assertTemplateUsed(response, 'internments/html/internment_history.html')
