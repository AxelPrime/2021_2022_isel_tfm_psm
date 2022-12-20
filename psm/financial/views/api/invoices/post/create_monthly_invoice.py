import random
from datetime import date
from functools import reduce

from asgiref.sync import sync_to_async
from django.db import transaction
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from financial.models import DailyValue, MonthlyInvoice
from financial.serializers.invoices import CreateInvoiceSerializer
from financial.utils.invoice_creation import InvoiceCreation
from financial.utils.invoice_dates_encryption import DateEncryption
from internment_management.models import CareHouseInternment
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from utils.dates.date_range import date_range

ALLOWED_USER_TYPES = [
    'care_house_staff',
    'superuser'
]


@sync_to_async()
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_monthly_invoice_api(request):
    # Obtain the authenticated user.
    user = request.user  # type: CustomUser
    # Check if the user has access permissions.
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissões de acesso',
        )
    # Get the request data.
    request_data = {
        "typology": request.data.get("typology"),
        "care_house": request.data.get('care_house'),
        "dates_encrypted": request.COOKIES.get(request.data.get("typology"))
    }
    # Serialize the request.
    serialized_request = CreateInvoiceSerializer(data=request_data)
    # Validate the request.
    if not serialized_request.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Pedido inválido',
            data=serialized_request.errors
        )
    # Obtain the validated date.
    valid_data = serialized_request.validated_data

    # Verify if the care house has been selected for superuser.
    if user.user_type == 'superuser' and not valid_data['care_house']:
        return error_response(
            HTTP_400_BAD_REQUEST,
            "É necessário indicar a Casa de Saúde"
        )

    # Decrypt the invoice dates.
    date_encryption = DateEncryption()
    invoice_start_date, invoice_end_date = date_encryption.decrypt(valid_data['dates_encrypted'])  # type: date

    # Define the base query.
    query = Q(admission_date__lte=invoice_end_date) & \
        (Q(leave_date__isnull=True) | Q(leave_date__lte=invoice_end_date)) & \
        Q(referral__typology=valid_data['typology'])

    # Choose the care house source.
    if user.user_type == 'care_house_staff':
        query &= Q(referral__care_house=user.care_house)
    else:
        query &= Q(referral__care_house__identification_code=valid_data['care_house'])

    # Obtain the list of internments.
    internments_list = CareHouseInternment.objects.prefetch_related('activitylog_set').filter(query)

    # Verify if the internments list is empty.
    if internments_list.count() == 0:
        return error_response(
            HTTP_404_NOT_FOUND,
            'Não foram encontrados pacientes com a tipologia pedida.'
        )

    # Obtain the daily values to apply.
    daily_values = DailyValue.objects.filter(
        Q(end_date__gte=invoice_start_date) |
        Q(end_date__isnull=True)
    ).order_by('start_date')

    # Instantiate the invoice creation class.
    invoice_creation = InvoiceCreation(
        date_range(invoice_start_date, invoice_end_date),
        internments_list,
        daily_values
    )

    # Obtain the invoice data.
    invoice_data = invoice_creation.get_invoice_data()
    invoice_data['total_amount'] = reduce(lambda a, b: a + b['total_amount'], invoice_data['data'], 0)
    invoice_data['total_patients'] = len(invoice_data['data'])

    with transaction.atomic():
        # Obtain the list of invoices created for the current month.
        monthly_invoices = MonthlyInvoice.objects.filter(
            month=invoice_start_date.month,
            year=invoice_start_date.year,
            typology=valid_data['typology']
        ).exclude(
            status='rejected'
        )

        # Verify if the list is empty.
        if monthly_invoices.count() > 0:
            return error_response(
                HTTP_409_CONFLICT,
                'Listagem já criada para o mês indicado.'
            )

        invoice = MonthlyInvoice(
            invoice_number=random.randint(0, 100000),
            care_house=user.care_house,
            typology=valid_data['typology'],
            invoice_lines=invoice_data,
            start_date=invoice_start_date,
            end_date=invoice_end_date,
            month=invoice_start_date.month,
            year=invoice_start_date.year,
            status='temp'
        )
        invoice.save()

    return success_response(
        True,
        'Listagem criada',
        data={
            'invoice_data': invoice_data
        }
    )
