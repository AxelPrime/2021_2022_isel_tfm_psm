from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.status import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from financial.models import MonthlyInvoice
from financial.serializers.invoices import EvaluateMonthlyInvoiceSerializer
from financial.utils.typology_ii import update_typology_ii_stats
from user_management.models import CustomUser
from utils.api_responses.responses import error_response, success_response
from asgiref.sync import sync_to_async
from financial.utils.yearly_stats import update_typology_stats
from financial.utils.yearly_invoices import update_yearly_invoice
from utils.notifications.notifications import NotificationsManager

ALLOWED_USER_TYPES = [
    'financial',
    'superuser',
]

NOTIFICATIONS_TO_CREATE = {
    "true": {
        "notification_template": "INVOICE_APPROVED",
        "notification_create_type": "invoice_evaluation",
        "readable": True,
        "link": "/care-house/finances/receipt-history/"
    },
    "false": {
        "notification_template": "INVOICE_REJECTED",
        "notification_create_type": "invoice_evaluation",
        "readable": True,
        "link": "/care-house/finances/receipt-history/"
    }
}


@sync_to_async()
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def evaluate_monthly_invoice_api(request):
    # Obtain the user from the request.
    user = request.user  # type: CustomUser
    # Check if the user has access permissions.
    if user.user_type not in ALLOWED_USER_TYPES:
        return error_response(
            HTTP_401_UNAUTHORIZED,
            'Utilizador sem permissões de acesso',
        )

    # Serialize the request body.
    serialized_request = EvaluateMonthlyInvoiceSerializer(data=request.data)
    # Velidate the data.
    if not serialized_request.is_valid():
        return error_response(
            HTTP_400_BAD_REQUEST,
            'Pedido inválido',
            data=serialized_request.errors
        )
    # Obtain the validated data.
    valid_data = serialized_request.validated_data
    # Begin transaction.
    with transaction.atomic():
        # Obtain the invoice.
        try:
            invoice = MonthlyInvoice.objects.get(invoice_number=valid_data['invoice_number'])
        except MonthlyInvoice.DoesNotExist:
            return error_response(
                HTTP_404_NOT_FOUND,
                'Recibo não encontrado'
            )

        notification_data = NOTIFICATIONS_TO_CREATE.get(valid_data['approve'])

        notification_manager = NotificationsManager(
            ["invoice_creation"],
            notification_data['notification_create_type']
        )

        # Set the evaluation.
        if valid_data['approve'] == 'true':
            invoice.status = 'paid'
            update_typology_stats(invoice)
            if invoice.typology == 'II':
                update_typology_ii_stats(invoice)
            else:
                update_yearly_invoice(invoice)
        else:
            if not valid_data['rejection_reason']:
                return error_response(
                    HTTP_400_BAD_REQUEST,
                    'É necessário indicar a razão de rejeição'
                )
            invoice.status = 'rejected'
            invoice.rejection_reason = valid_data['rejection_reason']

        # Save the data.
        invoice.save()

        notification_manager.create_notification(
            notification_for="care_house_staff",
            template=notification_data['notification_template'],
            readable=notification_data['readable'],
            redirect_to=notification_data['link'],
            referral=None,
            invoice=invoice,
            care_house=invoice.care_house,
        )
        notification_manager.hide_notification(
            notification_for="financial",
            referral=None,
            invoice=invoice
        )
    return success_response(False, 'Recibo avaliado')
