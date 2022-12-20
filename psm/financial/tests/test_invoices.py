import calendar
from datetime import datetime, date
from http.cookies import SimpleCookie

from django.test import TestCase

from financial.models import MonthlyInvoice
from financial.utils.invoice_dates_encryption import DateEncryption
from utils.test_data import *


class TestInvoices(TestCase):
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

    def create_monthly_invoice(self):
        date_today = datetime.utcnow()
        year = date_today.year if date_today.month != 1 else date_today.year - 1
        month = date_today.month - 1
        date_range = calendar.monthrange(year, month)
        date_encryption = DateEncryption()
        date_encrypted = date_encryption.encrypt(
            date(year=year, month=month, day=1),
            date(year=year, month=month, day=date_range[1])
        )
        typology = 'II'

        # Perform the login.
        login_data = {
            'email': 'care_house@mail.com',
            'password': 'caranguejo2k9',
            'remember_user': False
        }
        self.client.post('/api/users/login/', data=login_data, content_type='application/json', follow=True)

        request_body = {
            'typology': typology,
        }

        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.client.cookies.get("userToken").value}'
        }

        self.client.cookies = SimpleCookie({
            'II': date_encrypted
        })

        response = self.client.post('/api/invoices/monthly-invoices/create/', data=request_body, follow=True, **headers)
        self.assertEquals(201, response.status_code)
        invoice = MonthlyInvoice.objects.all().first()
        self.assertIsNotNone(invoice)

    def finalize_monthly_invoice(self):
        invoice = MonthlyInvoice.objects.all().last()
        file1 = open('files/test/file1.txt', 'rb')
        # Perform the login.
        login_data = {
            'email': 'care_house@mail.com',
            'password': 'caranguejo2k9',
            'remember_user': False
        }
        self.client.post('/api/users/login/', data=login_data, content_type='application/json', follow=True)

        request_body = {
            'invoice_number': invoice.invoice_number,
            'invoice_file': file1,
        }

        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.client.cookies.get("userToken").value}'
        }

        response = self.client.post('/api/invoices/monthly-invoices/finalize/', data=request_body, follow=True,
                                    **headers)
        self.assertEquals(200, response.status_code)
        invoice = MonthlyInvoice.objects.all().first()
        self.assertIsNotNone(invoice)

    def evaluate_invoice(self):
        invoice = MonthlyInvoice.objects.all().last()
        file1 = open('files/test/file1.txt', 'rb')
        # Perform the login.
        login_data = {
            'email': 'financial@mail.com',
            'password': 'caranguejo2k9',
            'remember_user': False
        }
        self.client.post('/api/users/login/', data=login_data, content_type='application/json', follow=True)

        request_body = {
            'invoice_number': invoice.invoice_number,
            'approve': "true",
            'rejection_reason': "",
        }

        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.client.cookies.get("userToken").value}'
        }

        response = self.client.post('/api/invoices/monthly-invoices/evaluate/', data=request_body, follow=True,
                                    **headers)
        self.assertEquals(200, response.status_code)
        invoice = MonthlyInvoice.objects.all().first()
        self.assertIsNotNone(invoice)

    def test_invoice_process(self):
        self.create_monthly_invoice()
        self.finalize_monthly_invoice()
        self.evaluate_invoice()
