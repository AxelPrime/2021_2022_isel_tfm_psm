from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from asgiref.sync import sync_to_async

from financial.models import MonthlyInvoice
from utils.api_responses.responses import error_response, success_response
from financial.serializers.invoices import FinalizeInvoiceDataSerializer, FinalizeInvoiceFileSerializer

from user_management.models import CustomUser
from utils.notifications.notifications import NotificationsManager

ALLOWED_USER_TYPES = [
    'care_house_staff',
    'superuser'
]

NOTIFICATION_CREATE_TEMPLATE = "INVOICE_CREATION"
NOTIFICATION_CREATE_TYPE = "invoice_creation"


@sync_to_async()
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def finalize_monthly_invoice_api(request):
    user = request.user  # type: CustomUser
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(HTTP_401_UNAUTHORIZED, 'Utilizador sem permissões de acesso')

    # Serialize the request data.
    serialized_data = FinalizeInvoiceDataSerializer(data=request.POST)
    serialized_file = FinalizeInvoiceFileSerializer(data=request.FILES)

    # Validate the data.
    if not serialized_data.is_valid() or not serialized_file.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Pedido inválido',
            data={
                'data': serialized_data.errors,
                'file': serialized_file.errors
            }
        )

    # Obtain the valid data.
    valid_data = serialized_data.validated_data
    valid_file = serialized_file.validated_data

    # Instantiate the notification manager.
    notifications_manager = NotificationsManager("", NOTIFICATION_CREATE_TYPE)

    # Begin transaction.
    with transaction.atomic():
        # Obtain the invoice.
        try:
            invoice = MonthlyInvoice.objects.get(invoice_number=valid_data['invoice_number'])
        except MonthlyInvoice.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                'Listagem não encontrada'
            )

        # Set the file.
        invoice.invoice_file = valid_file['invoice_file']
        # Set the status as pending approval.
        invoice.status = "awaits_payment"

        # Save the invoice.
        invoice.save()

        notifications_manager.create_notification(
            notification_for="financial",
            template=NOTIFICATION_CREATE_TEMPLATE,
            readable=False,
            redirect_to="/financial/finances/monthly-receipts/",
            referral=None,
            invoice=invoice,
            care_house=invoice.care_house
        )

    return success_response(
        False,
        'Listagem finalizada'
    )
